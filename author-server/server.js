import express from 'express';
import { Octokit } from '@octokit/rest';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// GITHUB_TOKEN muss in der docker-compose als Environment-Variable übergeben werden
const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
const OWNER = 'marcodem';
const REPO = 'sanskritkurs-payer';
const DRAFTS_BRANCH = 'author-drafts';
const MAIN_BRANCH = 'main';

// VitePress dist-author Dateien werden von hier ausgeliefert, mit Support für Clean URLs (.html)
app.use(express.static(path.join(__dirname, 'public'), { extensions: ['html'] }));

app.get('/api/load', async (req, res) => {
    const { filepath } = req.query; // z.B. docs/lektionen/lektion01.md
    if (!filepath) return res.status(400).json({ error: 'Missing filepath' });

    try {
        let content;
        // 1. Zuerst versuchen wir, die Datei aus dem Draft-Branch zu laden
        try {
            const draftResponse = await octokit.rest.repos.getContent({
                owner: OWNER,
                repo: REPO,
                path: filepath,
                ref: DRAFTS_BRANCH
            });
            content = Buffer.from(draftResponse.data.content, 'base64').toString('utf8');
        } catch (e) {
            // 2. Falls sie im Draft-Branch nicht existiert, laden wir sie vom Main-Branch
            const mainResponse = await octokit.rest.repos.getContent({
                owner: OWNER,
                repo: REPO,
                path: filepath,
                ref: MAIN_BRANCH
            });
            content = Buffer.from(mainResponse.data.content, 'base64').toString('utf8');
        }

        res.json({ content });
    } catch (error) {
        console.error('Error loading file:', error.message);
        res.status(500).json({ error: 'File not found on GitHub or error accessing API' });
    }
});

app.post('/api/save', async (req, res) => {
    const { filepath, content } = req.body;
    if (!filepath || !content) return res.status(400).json({ error: 'Missing filepath or content' });

    try {
        // 1. Prüfen, ob der Drafts-Branch existiert, ansonsten erstellen
        let branchExists = true;
        try {
            await octokit.rest.repos.getBranch({ owner: OWNER, repo: REPO, branch: DRAFTS_BRANCH });
        } catch (e) {
            branchExists = false;
        }

        if (!branchExists) {
            const mainRef = await octokit.rest.git.getRef({
                owner: OWNER, repo: REPO, ref: `heads/${MAIN_BRANCH}`
            });
            await octokit.rest.git.createRef({
                owner: OWNER, repo: REPO, ref: `refs/heads/${DRAFTS_BRANCH}`, sha: mainRef.data.object.sha
            });
        }

        // 2. Prüfen, ob die Datei im Draft-Branch schon existiert, um den SHA zu erhalten
        let sha = null;
        try {
            const fileData = await octokit.rest.repos.getContent({
                owner: OWNER, repo: REPO, path: filepath, ref: DRAFTS_BRANCH
            });
            sha = fileData.data.sha;
        } catch (e) {}

        // 3. Datei im Draft-Branch aktualisieren oder erstellen
        await octokit.rest.repos.createOrUpdateFileContents({
            owner: OWNER,
            repo: REPO,
            path: filepath,
            message: `Redaktionelle Änderung: ${filepath}`,
            content: Buffer.from(content).toString('base64'),
            branch: DRAFTS_BRANCH,
            ...(sha ? { sha } : {}) // SHA nur senden, wenn Datei existiert
        });

        // 4. Prüfen, ob bereits ein Pull Request existiert, ansonsten erstellen
        try {
            const prs = await octokit.rest.pulls.list({
                owner: OWNER, repo: REPO, head: `${OWNER}:${DRAFTS_BRANCH}`, base: MAIN_BRANCH, state: 'open'
            });

            if (prs.data.length === 0) {
                await octokit.rest.pulls.create({
                    owner: OWNER,
                    repo: REPO,
                    title: 'Redaktionelle Änderungen (QA-Viewer)',
                    head: DRAFTS_BRANCH,
                    base: MAIN_BRANCH,
                    body: 'Automatischer Pull Request des QA-Viewers.\nBitte Änderungen im "Files changed" Tab prüfen und dann mergen.'
                });
            }
        } catch (e) {
            console.error('Error checking/creating PR:', e.message);
        }

        res.json({ success: true, message: 'Gespeichert in GitHub (author-drafts)' });
    } catch (error) {
        console.error('Error saving file:', error.message);
        res.status(500).json({ error: 'Failed to save to GitHub' });
    }
});

const PORT = process.env.PORT || 80;
app.listen(PORT, () => {
    console.log(`Author server listening on port ${PORT}`);
});
