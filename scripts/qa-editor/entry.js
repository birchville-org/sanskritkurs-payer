// CodeMirror 6 editor for docs/public/qa_viewer.html.
// Bundled to docs/public/qa_editor.js (npm run build:qa-editor).
// Exposes window.QaEditor.create(textarea) with the small CodeMirror-5-style
// API that qa_viewer.html already uses (getValue, setValue, setOption, ...).
import { Compartment, EditorState, RangeSetBuilder, StateField } from '@codemirror/state';
import {
  Decoration,
  EditorView,
  drawSelection,
  keymap,
  lineNumbers,
} from '@codemirror/view';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { defaultHighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { markdown } from '@codemirror/lang-markdown';
import { vim } from '@replit/codemirror-vim';

// Same container-nesting logic as the former updateCodeMirrorBlocks():
// each line gets block-l<depth>-<name> (max. 3 layers) and block-bg-<innermost>.
function computeBlockDecorations(doc) {
  const builder = new RangeSetBuilder();
  const stack = [];
  for (let n = 1; n <= doc.lines; n++) {
    const line = doc.line(n);
    const openMatch = line.text.match(/^(:{3,5})\s*([\w-]+)/);
    const closeMatch = line.text.trim().match(/^(:{3,5})$/);
    let toRemove = -1;
    if (openMatch) {
      stack.push({ level: openMatch[1].length, name: openMatch[2] });
    } else if (closeMatch) {
      for (let j = stack.length - 1; j >= 0; j--) {
        if (stack[j].level === closeMatch[1].length) {
          toRemove = j;
          break;
        }
      }
    }
    const classes = [];
    for (let d = 0; d < Math.min(stack.length, 3); d++) {
      classes.push(`block-l${d}-${stack[d].name}`);
    }
    if (stack.length > 0) classes.push(`block-bg-${stack[stack.length - 1].name}`);
    if (classes.length) {
      builder.add(line.from, line.from, Decoration.line({ class: classes.join(' ') }));
    }
    if (toRemove !== -1) stack.splice(toRemove, 1);
  }
  return builder.finish();
}

const blockField = StateField.define({
  create: (state) => computeBlockDecorations(state.doc),
  update: (deco, tr) => (tr.docChanged ? computeBlockDecorations(tr.state.doc) : deco),
  provide: (f) => EditorView.decorations.from(f),
});

const vimC = new Compartment();
const numC = new Compartment();
const numbers = (first) => lineNumbers({ formatNumber: (n) => String(n - 1 + first) });

// Returns the CodeMirror EditorView; onChange(view) fires on every document change.
function create(textarea, onChange) {
  const view = new EditorView({
    parent: textarea.parentNode,
    state: EditorState.create({
      doc: textarea.value,
      extensions: [
        vimC.of(vim()),
        numC.of(numbers(1)),
        history(),
        drawSelection(),
        keymap.of([...defaultKeymap, ...historyKeymap]),
        markdown(),
        syntaxHighlighting(defaultHighlightStyle),
        EditorView.lineWrapping,
        blockField,
        EditorView.updateListener.of((u) => {
          if (u.docChanged && onChange) onChange(u.view);
        }),
      ],
    }),
  });
  textarea.style.display = 'none';
  return view;
}

const setDoc = (view, text, options = {}) => {
  if (options && options.preserveState) {
    const prevSel = view.state.selection ? view.state.selection.main : null;
    const prevScrollTop = view.scrollDOM ? view.scrollDOM.scrollTop : 0;
    const prevScrollLeft = view.scrollDOM ? view.scrollDOM.scrollLeft : 0;
    const maxPos = text.length;
    const update = { changes: { from: 0, to: view.state.doc.length, insert: text } };
    if (prevSel) {
      update.selection = {
        anchor: Math.min(prevSel.anchor, maxPos),
        head: Math.min(prevSel.head, maxPos),
      };
    }
    view.dispatch(update);
    if (view.scrollDOM) {
      view.scrollDOM.scrollTop = prevScrollTop;
      view.scrollDOM.scrollLeft = prevScrollLeft;
    }
    return;
  }
  view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } });
};

const setFirstLine = (view, first) =>
  view.dispatch({ effects: numC.reconfigure(numbers(first)) });

const setVim = (view, on) =>
  view.dispatch({ effects: vimC.reconfigure(on ? vim() : []) });

window.QaEditor = { create, setDoc, setFirstLine, setVim };
