import { a2 as rest_props, a3 as fallback, a4 as spread_attributes, _ as slot, Y as bind_props, R as pop, $ as sanitize_props, P as push } from "./index.js";
import { h as cn } from "./projects.js";
function Card_footer($$payload, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const $$restProps = rest_props($$sanitized_props, ["class"]);
  push();
  let className = fallback($$props["class"], void 0);
  $$payload.out += `<div${spread_attributes({
    class: cn("flex items-center p-6 pt-0", className),
    ...$$restProps
  })}><!---->`;
  slot($$payload, $$props, "default", {}, null);
  $$payload.out += `<!----></div>`;
  bind_props($$props, { class: className });
  pop();
}
export {
  Card_footer as C
};
