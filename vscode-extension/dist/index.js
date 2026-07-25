var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  try {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  } catch (e) {
    throw mod = 0, e;
  }
};

// node_modules/markdown-it-container/index.js
var require_markdown_it_container = __commonJS({
  "node_modules/markdown-it-container/index.js"(exports2, module2) {
    "use strict";
    module2.exports = function container_plugin(md, name, options) {
      function validateDefault(params) {
        return params.trim().split(" ", 2)[0] === name;
      }
      function renderDefault(tokens, idx, _options, env, slf) {
        if (tokens[idx].nesting === 1) {
          tokens[idx].attrJoin("class", name);
        }
        return slf.renderToken(tokens, idx, _options, env, slf);
      }
      options = options || {};
      var min_markers = 3, marker_str = options.marker || ":", marker_char = marker_str.charCodeAt(0), marker_len = marker_str.length, validate = options.validate || validateDefault, render = options.render || renderDefault;
      function container(state, startLine, endLine, silent) {
        var pos, nextLine, marker_count, markup, params, token, old_parent, old_line_max, auto_closed = false, start = state.bMarks[startLine] + state.tShift[startLine], max = state.eMarks[startLine];
        if (marker_char !== state.src.charCodeAt(start)) {
          return false;
        }
        for (pos = start + 1; pos <= max; pos++) {
          if (marker_str[(pos - start) % marker_len] !== state.src[pos]) {
            break;
          }
        }
        marker_count = Math.floor((pos - start) / marker_len);
        if (marker_count < min_markers) {
          return false;
        }
        pos -= (pos - start) % marker_len;
        markup = state.src.slice(start, pos);
        params = state.src.slice(pos, max);
        if (!validate(params, markup)) {
          return false;
        }
        if (silent) {
          return true;
        }
        nextLine = startLine;
        for (; ; ) {
          nextLine++;
          if (nextLine >= endLine) {
            break;
          }
          start = state.bMarks[nextLine] + state.tShift[nextLine];
          max = state.eMarks[nextLine];
          if (start < max && state.sCount[nextLine] < state.blkIndent) {
            break;
          }
          if (marker_char !== state.src.charCodeAt(start)) {
            continue;
          }
          if (state.sCount[nextLine] - state.blkIndent >= 4) {
            continue;
          }
          for (pos = start + 1; pos <= max; pos++) {
            if (marker_str[(pos - start) % marker_len] !== state.src[pos]) {
              break;
            }
          }
          if (Math.floor((pos - start) / marker_len) < marker_count) {
            continue;
          }
          pos -= (pos - start) % marker_len;
          pos = state.skipSpaces(pos);
          if (pos < max) {
            continue;
          }
          auto_closed = true;
          break;
        }
        old_parent = state.parentType;
        old_line_max = state.lineMax;
        state.parentType = "container";
        state.lineMax = nextLine;
        token = state.push("container_" + name + "_open", "div", 1);
        token.markup = markup;
        token.block = true;
        token.info = params;
        token.map = [startLine, nextLine];
        state.md.block.tokenize(state, startLine + 1, nextLine);
        token = state.push("container_" + name + "_close", "div", -1);
        token.markup = state.src.slice(start, pos);
        token.block = true;
        state.parentType = old_parent;
        state.lineMax = old_line_max;
        state.line = nextLine + (auto_closed ? 1 : 0);
        return true;
      }
      md.block.ruler.before("fence", "container_" + name, container, {
        alt: ["paragraph", "reference", "blockquote", "list"]
      });
      md.renderer.rules["container_" + name + "_open"] = render;
      md.renderer.rules["container_" + name + "_close"] = render;
    };
  }
});

// node_modules/markdown-it-extensible/index.js
var require_markdown_it_extensible = __commonJS({
  "node_modules/markdown-it-extensible/index.js"(exports2, module2) {
    var fs = require("fs");
    var path = require("path");
    var container = require_markdown_it_container();
    var cachedCss = "";
    try {
      cachedCss = fs.readFileSync(path.join(__dirname, "vscode-extension/media/payer-theme.css"), "utf8");
    } catch (e) {
    }
    module2.exports = function scholarlyPlugin(md, options = {}) {
      const injectStyles = options.injectStyles !== false;
      if (injectStyles && cachedCss) {
        md.core.ruler.push("extensible_styles_inject", (state) => {
          if (state.tokens.length > 0 && !state.env.__extensibleStylesInjected) {
            state.env.__extensibleStylesInjected = true;
            const styleToken = new state.Token("html_block", "", 0);
            styleToken.content = `<style>
${cachedCss}
</style>
`;
            state.tokens.unshift(styleToken);
          }
        });
      }
      const blockContainers = options.blockContainers && options.blockContainers.length > 0 ? options.blockContainers : [
        { name: "grammar-box", className: "grammar-box" },
        { name: "grammarbox", className: "grammar-box" },
        { name: "grammar-box2", className: "grammar-box2" },
        { name: "grammarbox2", className: "grammar-box2" },
        { name: "media", className: "media" },
        { name: "center", className: "center" },
        { name: "metrik-schema", className: "metrik-schema" },
        { name: "metrikschema", className: "metrik-schema" },
        { name: "important", className: "important" },
        { name: "deleteme-box", className: "deleteme-box" },
        { name: "deletemebox", className: "deleteme-box" },
        { name: "note-box", className: "note-box" },
        { name: "notebox", className: "note-box" },
        { name: "laut-table", className: "laut-table" },
        { name: "lauttable", className: "laut-table" },
        { name: "indent", className: "indent" },
        { name: "compact", className: "compact" },
        { name: "no-header", className: "no-header" },
        { name: "noheader", className: "no-header" }
      ];
      blockContainers.forEach((containerOpt) => {
        const box = containerOpt.name;
        const cssClass = containerOpt.className;
        md.use(container, box, {
          validate: (params) => params.trim().match(new RegExp(`^${box}(?:\\s+(.*))?$`)),
          render: (tokens, idx) => {
            const m = tokens[idx].info.trim().match(new RegExp(`^${box}(?:\\s+(.*))?$`));
            if (tokens[idx].nesting === 1) {
              let titleHtml = "";
              if (m && m[1]) {
                const titleMatch = m[1].match(/^\[([^\]]+)\]/);
                if (titleMatch) {
                  titleHtml = `<div class="md-box__title">${titleMatch[1]}</div>
`;
                }
              }
              return `<div class="${cssClass} custom-block">
${titleHtml}`;
            } else {
              return `</div>
`;
            }
          }
        });
      });
      try {
        md.core.ruler.before("curly_attributes", "table_meta_fix", (state) => {
          for (let i = 0; i < state.tokens.length; i++) {
            const token = state.tokens[i];
            if (token.type === "tbody_close") {
              token.type = "tbody_close_temp";
            }
          }
        });
        md.core.ruler.after("curly_attributes", "table_meta_restore", (state) => {
          for (let i = 0; i < state.tokens.length; i++) {
            const token = state.tokens[i];
            if (token.type === "tbody_close_temp") {
              token.type = "tbody_close";
            }
          }
        });
      } catch (e) {
      }
      const inlineDirectives = options.inlineDirectives && options.inlineDirectives.length > 0 ? options.inlineDirectives : [
        { name: "sig", className: "signalrot", tag: "strong" },
        { name: "mark", className: "marker-yellow", tag: "mark" }
      ];
      const directiveMap = /* @__PURE__ */ new Map();
      inlineDirectives.forEach((dir) => {
        directiveMap.set(dir.name, {
          className: dir.className || dir.name,
          tag: dir.tag || "span"
        });
      });
      const getScholarlyRe = (inTable = false) => inTable ? /([⟪《][^⟫⟩》]+[⟫⟩》](?:\s*\|\|?)?|(?<!:):[a-zA-Z0-9_-]+\[.*?\]|(?<!:):br|(?<!:):indent)/g : /([⟪《][^⟫⟩》]+[⟫⟩》](?:\s*\|\|?)?|(?<!:):[a-zA-Z0-9_-]+\[.*?\])/g;
      md.core.ruler.after("linkify", "scholarly_fixes", (state) => {
        let insideTable = false;
        for (let i = 0; i < state.tokens.length; i++) {
          const token = state.tokens[i];
          if (token.type === "table_open") {
            insideTable = true;
          } else if (token.type === "table_close") {
            insideTable = false;
          }
          if (token.type !== "inline") continue;
          let newChildren = [];
          token.children?.forEach((child) => {
            if (child.type !== "text") {
              newChildren.push(child);
              return;
            }
            if (!getScholarlyRe(insideTable).test(child.content)) {
              newChildren.push(child);
              return;
            }
            function processContent(content) {
              const parts = content.split(getScholarlyRe(insideTable));
              parts.forEach((part) => {
                if (!part) return;
                if (part.match(/^[⟪《].*[⟫⟩》](?:\s*\|\|?)?$/)) {
                  let innerText = part.replace(/^[⟪《]|(?:[⟫⟩》](?:\s*\|\|?)?)$/g, "");
                  let dandaHtml = "";
                  const pipeMatchOutside = part.match(/[⟫⟩》](\s*)(\|\|?)$/);
                  if (pipeMatchOutside) {
                    const space = pipeMatchOutside[1];
                    const pipe = pipeMatchOutside[2];
                    const danda = pipe === "||" ? "\u0965" : "\u0964";
                    dandaHtml = `${space}${danda}`;
                  } else {
                    const pipeMatchInside = innerText.match(/(\s*)(\|\|?)$/);
                    if (pipeMatchInside) {
                      const space = pipeMatchInside[1];
                      const pipe = pipeMatchInside[2];
                      const danda = pipe === "||" ? "\u0965" : "\u0964";
                      dandaHtml = `${space}${danda}`;
                      innerText = innerText.slice(0, -pipeMatchInside[0].length);
                    }
                  }
                  const span = new state.Token("html_inline", "", 0);
                  span.content = `<span class="sanskrit-dev" translate="no" lang="sa">${innerText}${dandaHtml}</span>`;
                  newChildren.push(span);
                } else if (part.match(/^:[a-zA-Z0-9_-]+\[.*\]$/)) {
                  const colonPos = part.indexOf(":");
                  const bracketPos = part.indexOf("[");
                  const dirName = part.slice(colonPos + 1, bracketPos);
                  const innerText = part.slice(bracketPos + 1, -1);
                  const config = directiveMap.get(dirName) || { className: dirName, tag: "span" };
                  const tagName = config.tag || "span";
                  const className = config.className || dirName;
                  const openTag = new state.Token("html_inline", "", 0);
                  openTag.content = `<${tagName} class="${className}">`;
                  newChildren.push(openTag);
                  processContent(innerText);
                  const closeTag = new state.Token("html_inline", "", 0);
                  closeTag.content = `</${tagName}>`;
                  newChildren.push(closeTag);
                } else if (part === ":br" && insideTable) {
                  newChildren.push(new state.Token("hardbreak", "br", 0));
                } else if (part === ":indent" && insideTable) {
                  const span = new state.Token("html_inline", "", 0);
                  span.content = '<span class="indent-inline"></span>';
                  newChildren.push(span);
                } else {
                  const text = new state.Token("text", "", 0);
                  text.content = part;
                  newChildren.push(text);
                }
              });
            }
            processContent(child.content);
          });
          token.children = newChildren;
        }
      });
    };
  }
});

// src/index.js
var extensiblePlugin = require_markdown_it_extensible();
var vscode = require("vscode");
function activate(context) {
  return {
    extendMarkdownIt(md) {
      const config = vscode.workspace.getConfiguration("extensibleMarkdown");
      const blockContainers = config.get("blockContainers") || [];
      return md.use(extensiblePlugin, {
        blockContainers
      });
    }
  };
}
module.exports = {
  activate
};
