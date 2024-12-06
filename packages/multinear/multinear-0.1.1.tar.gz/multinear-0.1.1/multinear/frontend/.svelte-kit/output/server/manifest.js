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
		client: {"start":"_app/immutable/entry/start.uF4iCYlv.js","app":"_app/immutable/entry/app.CQJF7shZ.js","imports":["_app/immutable/entry/start.uF4iCYlv.js","_app/immutable/chunks/entry.CGI9eiKr.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/entry/app.CQJF7shZ.js","_app/immutable/chunks/index-client.CTjIiTiR.js","_app/immutable/chunks/disclose-version.DJKRdGjo.js","_app/immutable/chunks/props.hsVcazBB.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
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
