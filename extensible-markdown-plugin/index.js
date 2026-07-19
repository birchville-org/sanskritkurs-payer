const container = require('markdown-it-container');

module.exports = function scholarlyPlugin(md, options = {}) {
  // 1. Custom Boxes (dynamically configurable, with static fallbacks for backward compatibility)
  const blockContainers = (options.blockContainers && options.blockContainers.length > 0) 
    ? options.blockContainers 
    : [
        { name: 'grammar-box', className: 'grammar-box' },
        { name: 'grammarbox', className: 'grammar-box' },
        { name: 'grammar-box2', className: 'grammar-box2' },
        { name: 'grammarbox2', className: 'grammar-box2' },
        { name: 'media', className: 'media' },
        { name: 'center', className: 'center' },
        { name: 'metrik-schema', className: 'metrik-schema' },
        { name: 'metrikschema', className: 'metrik-schema' },
        { name: 'important', className: 'important' },
        { name: 'deleteme-box', className: 'deleteme-box' },
        { name: 'deletemebox', className: 'deleteme-box' },
        { name: 'note-box', className: 'note-box' },
        { name: 'notebox', className: 'note-box' },
        { name: 'laut-table', className: 'laut-table' },
        { name: 'lauttable', className: 'laut-table' },
        { name: 'indent', className: 'indent' },
        { name: 'compact', className: 'compact' },
        { name: 'no-header', className: 'no-header' },
        { name: 'noheader', className: 'no-header' }
      ];

  blockContainers.forEach(containerOpt => {
    const box = containerOpt.name;
    const cssClass = containerOpt.className;
    md.use(container, box, {
      validate: (params) => params.trim().match(new RegExp(`^${box}(?:\\s+(.*))?$`)),
      render: (tokens, idx) => {
        const m = tokens[idx].info.trim().match(new RegExp(`^${box}(?:\\s+(.*))?$`));
        if (tokens[idx].nesting === 1) {
          let titleHtml = '';
          if (m && m[1]) {
            const titleMatch = m[1].match(/^\[([^\]]+)\]/);
            if (titleMatch) {
              titleHtml = `<div class="md-box__title">${titleMatch[1]}</div>\n`;
            }
          }
          return `<div class="${cssClass} custom-block">\n${titleHtml}`;
        } else {
          return `</div>\n`;
        }
      }
    });
  });

  // 2. Fix for markdown-it-attrs tables tbody calculate error with markdown-it-multimd-table
  // Temporarily rename tbody_close to bypass the buggy calculate rule
  md.core.ruler.before('curly_attributes', 'table_meta_fix', (state) => {
    for (let i = 0; i < state.tokens.length; i++) {
      const token = state.tokens[i];
      if (token.type === 'tbody_close') {
        token.type = 'tbody_close_temp';
      }
    }
  });

  // Restore tbody_close after curly_attributes has finished
  md.core.ruler.after('curly_attributes', 'table_meta_restore', (state) => {
    for (let i = 0; i < state.tokens.length; i++) {
      const token = state.tokens[i];
      if (token.type === 'tbody_close_temp') {
        token.type = 'tbody_close';
      }
    }
  });

  // 3. Scholarly syntax: :br, :indent, ⟪Devanagari⟫
  md.core.ruler.after('linkify', 'scholarly_fixes', (state) => {
    state.tokens.forEach(token => {
      if (token.type !== 'inline') return;
      let newChildren = [];
      token.children?.forEach(child => {
        if (child.type !== 'text') {
          newChildren.push(child);
          return;
        }

        const SCHOLARLY_RE = /([⟪《][^⟫⟩》]+[⟫⟩》](?:\s*\|\|?)?|sig\[.*?\]|(?<!:):br|(?<!:):indent)/g;
        if (!SCHOLARLY_RE.test(child.content)) {
          newChildren.push(child);
          return;
        }

        function processContent(content, isInsideSig = false) {
          const parts = content.split(SCHOLARLY_RE);
          parts.forEach(part => {
            if (!part) return;
            if (part.match(/^[⟪《].*[⟫⟩》](?:\s*\|\|?)?$/)) {
              let innerText = part.replace(/^[⟪《]|(?:[⟫⟩》](?:\s*\|\|?)?)$/g, '');
              let dandaHtml = '';

              // Check outside first:
              const pipeMatchOutside = part.match(/[⟫⟩》](\s*)(\|\|?)$/);
              if (pipeMatchOutside) {
                const space = pipeMatchOutside[1];
                const pipe = pipeMatchOutside[2];
                const danda = pipe === '||' ? '॥' : '।';
                dandaHtml = `${space}${danda}`;
              } else {
                // Check inside:
                const pipeMatchInside = innerText.match(/(\s*)(\|\|?)$/);
                if (pipeMatchInside) {
                  const space = pipeMatchInside[1];
                  const pipe = pipeMatchInside[2];
                  const danda = pipe === '||' ? '॥' : '।';
                  dandaHtml = `${space}${danda}`;
                  innerText = innerText.slice(0, -pipeMatchInside[0].length);
                }
              }

              const span = new state.Token('html_inline', '', 0);
              span.content = `<span class="sanskrit-dev" translate="no" lang="sa">${innerText}${dandaHtml}</span>`;
              newChildren.push(span);
            } else if (part.match(/^sig\[.*\]$/) && !isInsideSig) {
              const spanOpen = new state.Token('html_inline', '', 0);
              spanOpen.content = `<strong class="signalrot">`;
              newChildren.push(spanOpen);

              processContent(part.slice(4, -1), true);

              const spanClose = new state.Token('html_inline', '', 0);
              spanClose.content = `</strong>`;
              newChildren.push(spanClose);
            } else if (part === ':br') {
              newChildren.push(new state.Token('hardbreak', 'br', 0));
            } else if (part === ':indent') {
              const span = new state.Token('html_inline', '', 0);
              span.content = '<span class="indent-inline"></span>';
              newChildren.push(span);
            } else {
              const text = new state.Token('text', '', 0);
              text.content = part;
              newChildren.push(text);
            }
          });
        }

        processContent(child.content);
      });
      token.children = newChildren;
    });
  });
};
