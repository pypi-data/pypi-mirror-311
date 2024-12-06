import * as universal from '../entries/pages/_layout.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+layout.ts";
export const imports = ["_app/immutable/nodes/0.BV0K8Fs8.js","_app/immutable/chunks/disclose-version.DJKRdGjo.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/chunks/projects.Dr8v4MvC.js","_app/immutable/chunks/entry.CGI9eiKr.js","_app/immutable/chunks/legacy.RfLVu9Ez.js","_app/immutable/chunks/index.-62bZizV.js","_app/immutable/chunks/props.hsVcazBB.js","_app/immutable/chunks/stores.Da7ADmB3.js","_app/immutable/chunks/index.CXFO8A2a.js"];
export const stylesheets = ["_app/immutable/assets/0.YBB7ZK2Z.css"];
export const fonts = [];
