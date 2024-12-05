export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.ico"]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.Bg5Df2XY.js","app":"_app/immutable/entry/app.q4an4vAD.js","imports":["_app/immutable/entry/start.Bg5Df2XY.js","_app/immutable/chunks/entry.CTB_l6bl.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/entry/app.q4an4vAD.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/chunks/disclose-version.DJKRdGjo.js","_app/immutable/chunks/props.hsVcazBB.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js'))
		],
		routes: [
			
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
