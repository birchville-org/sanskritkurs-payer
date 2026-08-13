-- Pandoc Lua Filter to convert project custom Markdown structures to Typst components

function Inline(el)
  if el.t == "Str" then
    -- Handle ⟪...⟫
    local text = el.text
    if text:find("⟪") then
      text = text:gsub("⟪([^⟫]+)⟫", function(inside)
        if inside:find("[\u{0900}-\u{097F}]") then
          return "#dev[" .. inside .. "]"
        else
          return "#iast[" .. inside .. "]"
        end
      end)
      return pandoc.RawInline('typst', text)
    end
  end
  return el
end

function Span(el)
  if el.classes:includes("sanskrit-dev") then
    return pandoc.RawInline('typst', '#dev[' .. pandoc.utils.stringify(el.content) .. ']')
  elseif el.classes:includes("sig") then
    return pandoc.RawInline('typst', '#sig[' .. pandoc.utils.stringify(el.content) .. ']')
  end
  return el
end

function Div(el)
  if el.classes:includes("grammar-box") then
    return {
      pandoc.RawBlock('typst', '#grammarbox['),
      el,
      pandoc.RawBlock('typst', ']')
    }
  elseif el.classes:includes("center") then
    return {
      pandoc.RawBlock('typst', '#centerbox['),
      el,
      pandoc.RawBlock('typst', ']')
    }
  elseif el.classes:includes("indent") then
    return {
      pandoc.RawBlock('typst', '#indentbox['),
      el,
      pandoc.RawBlock('typst', ']')
    }
  end
  return el
end
