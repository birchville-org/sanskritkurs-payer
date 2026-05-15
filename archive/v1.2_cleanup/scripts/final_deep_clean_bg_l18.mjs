import fs from 'fs'
import path from 'path'

const filePath = 'docs/bg/lektionen/lektion18.md'
let content = fs.readFileSync(filePath, 'utf8')

// Fix random injections
content = content.replace(/> नास्ति कामसमो व्याधिर्\s*\n/g, '');
content = content.replace(/> तदन्यत्वं тadalpata ।\s*\n/g, '');

// Fix corrupted Sanskrit (Cyrillic мо)
content = content.replace(/कामसмо/g, 'कामसमो');

// Fix duplicated headers
content = content.replace(/### 18\.2\.1\. композити от тип सुकर \/ दुष्कर\s*\n\s*### 18\.2\.1\. композити от тип सुकर \/ दुष्कर/g, '### 18.2.1. композити от тип सुकर / दुष्कर');
content = content.replace(/### 18\.2\.1\. композити от тип सुकर \/ दुष्कर\s*\n\s*### 18\.2\.1\. композити от тип सुकर \/ दुष्कर/g, '### 18.2.1. композити от тип सुकर / दुष्कर'); // Twice just in case

// Fix incorrect examples under dus- (should be dus- examples)
const dusSectionStart = content.indexOf('दुс "лош, зъл"');
const dusSectionEnd = content.indexOf('### 18.2.1.');
if (dusSectionStart !== -1 && dusSectionEnd !== -1) {
    const dusSection = content.substring(dusSectionStart, dusSectionEnd);
    const correctDusExamples = `**Примери:**

> दुष्कृत n.: лошо дело
> 
> दुर्खादित 3: лошо сдъвкан
> 
> दुर्दुःख n.: голямо страдание
> 
> दुष्करण n.: лошо дело, трудно дело
> 
> सुकर 3: лесно за изпълнение (за сравнение)
> 
> दुर्गм 3: трудно за минаване
`;
    content = content.replace(dusSection, `दुс "лош, зъл" (вземете предвид сандхи!).\n\n${correctDusExamples}\n`);
}

// Fix vocabulary
content = content.replace(/ausgezeichnet, gut/g, 'отличен, добър');
content = content.replace(/Wasser/g, 'вода');
content = content.replace(/Ende, Grenze/g, 'край, граница');

// Remove the weird footer about "предишната секция"
content = content.replace(/\*Това е съдържанието на предишната секция, която вече беше зададена, така че в случай че искате да я разгледате пак, тук е\.\*/g, '');

fs.writeFileSync(filePath, content, 'utf8');
console.log('Deep cleaned BG Lektion 18');
