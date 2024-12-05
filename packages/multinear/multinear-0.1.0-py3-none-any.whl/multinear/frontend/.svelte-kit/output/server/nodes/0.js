import * as universal from '../entries/pages/_layout.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+layout.ts";
export const imports = ["_app/immutable/nodes/0.C5x88CxU.js","_app/immutable/chunks/disclose-version.DJKRdGjo.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/chunks/projects.B4n7Uloc.js","_app/immutable/chunks/entry.CTB_l6bl.js","_app/immutable/chunks/legacy.RfLVu9Ez.js","_app/immutable/chunks/index.btGWqnpN.js","_app/immutable/chunks/props.hsVcazBB.js","_app/immutable/chunks/stores.39RTRAIo.js","_app/immutable/chunks/index.D-v0UAeq.js"];
export const stylesheets = ["_app/immutable/assets/0.YBB7ZK2Z.css"];
export const fonts = [];
