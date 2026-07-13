const container = require('markdown-it-container');

module.exports = function scholarlyPlugin(md, options = {}) {
  // 1. Custom Boxes
  const customBoxes = {
    'grammar-box': 'grammar-box',
    'grammarbox': 'grammar-box',
    'grammar-box2': 'grammar-box2',
    'grammarbox2': 'grammar-box2',
    'media': 'media',
    'center': 'center',
    'metrik-schema': 'metrik-schema',
    'metrikschema': 'metrik-schema',
    'important': 'important',
    'deleteme-box': 'deleteme-box',
    'deletemebox': 'deleteme-box',
    'note-box': 'note-box',
    'notebox': 'note-box',
    'laut-table': 'laut-table',
    'lauttable': 'laut-table',
    'indent': 'indent',
    'compact': 'compact',
    'no-header': 'no-header',
    'noheader': 'no-header'
  };

  Object.keys(customBoxes).forEach(box => {
    const cssClass = customBoxes[box];
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
      if (token.type === 'inline') {
        let newChildren = [];
        token.children.forEach(child => {
          if (child.type === 'text') {
            const SCHOLARLY_RE = /([⟪《][^⟫⟩》]+[⟫⟩》]|sig\\[.*?\\]|(?<!:):br|(?<!:):indent)/g;
            if (!SCHOLARLY_RE.test(child.content)) {
              newChildren.push(child);
              return;
            }
            
            function processContent(content, isInsideSig = false) {
              const parts = content.split(SCHOLARLY_RE);
              parts.forEach(part => {
                if (!part) return;
                if (part.match(/^[⟪《].*[⟫⟩》]$/)) {
                  const span = new state.Token('html_inline', '', 0);
                  span.content = `<span class="sanskrit-dev" translate="no" lang="sa">${part.slice(1, -1)}</span>`;
                  newChildren.push(span);
                } else if (part.match(/^sig\\[.*\\]$/) && !isInsideSig) {
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
          } else {
            newChildren.push(child);
          }
        });
        token.children = newChildren;
      }
    });
  });
};
