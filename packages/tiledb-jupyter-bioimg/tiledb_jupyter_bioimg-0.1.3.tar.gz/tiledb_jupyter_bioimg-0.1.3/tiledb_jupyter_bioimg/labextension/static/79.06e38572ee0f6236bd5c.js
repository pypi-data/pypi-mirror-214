(()=>{var e,t,r={3281:(e,t,r)=>{"use strict";var a=r(3578),n=r.n(a),o=r(4551),s=r(9757),l=r(8399);const i={uint8:{bytes:Uint8Array.BYTES_PER_ELEMENT,format:s.Z.RED_INTEGER,internalFormat:s.Z.R8UI,type:s.Z.UNSIGNED_BYTE,filtering:s.Z.NEAREST,samplerType:"usampler2DArray",create:function(e){return new Uint8Array(e)}},uint16:{bytes:Uint16Array.BYTES_PER_ELEMENT,format:s.Z.RED_INTEGER,internalFormat:s.Z.R16UI,type:s.Z.UNSIGNED_SHORT,filtering:s.Z.NEAREST,samplerType:"usampler2DArray",create:function(e){return new Uint16Array(e)}},float16:{bytes:Float32Array.BYTES_PER_ELEMENT,format:s.Z.RED,internalFormat:s.Z.R16F,type:s.Z.FLOAT,filtering:s.Z.NEAREST,samplerType:"sampler2DArray",create:function(e){return new Float32Array(e)}},float32:{bytes:Float32Array.BYTES_PER_ELEMENT,format:s.Z.RED,internalFormat:s.Z.R32F,type:s.Z.FLOAT,filtering:s.Z.NEAREST,samplerType:"sampler2DArray",create:function(e){return new Float32Array(e)}}};class c{constructor(e,t){this.baseAxes=e,this.targetAxes=t,this.permutationMatrix=new Array(e.length);for(let e=0;e<this.baseAxes.length;++e){const t=this.targetAxes.indexOf(this.baseAxes[e]);this.permutationMatrix[e]=t}}reshape(e){const t=new Array(this.baseAxes.length);for(let r=0;r<this.baseAxes.length;++r)t[this.targetAxes.indexOf(this.baseAxes[r])]=e[r];return t}}function f(e){if(2===e.length)return e;const t=[];for(let r=0;r<e.length;r+=2)t.push([e[r],e[r+1]]);return t}function u(...e){const t=[],r=e.length-1;return function a(n,o){for(let s=0,l=e[o].length;s<l;s++){const l=n.slice(0);l.push(e[o][s]),o===r?t.push(l):a(l,o+1)}}([],0),t}function h(e){let t=1;const r=[];if(0===e.length)return r;for(let a=1;a<=e.length;a++)a===e.length||e[a]-e[a-1]!=1?(1===t?r.push([e[a-t],e[a-t]]):r.push([e[a-t],e[a-1]]),t=1):t++;return r}const d="TILEDB_BIOIMAGE_CACHE";let g=1;const p=async e=>{const t=await(0,l.X3)(d);return t.objectStoreNames.contains(e+"_1")?t:(t.close(),g=t.version+1,(0,l.X3)(d,g,{upgrade(t){for(let r=0;r<1;++r)t.objectStoreNames.contains(e+"_"+r)&&t.deleteObjectStore(e+"_"+r);t.createObjectStore(e+"_1",{autoIncrement:!0}).createIndex("timestamp","__timestamp")}}))},y=async(e,t)=>{const r=await p(e),a=await r.get(e+"_1",t);return r.close(),a},m=async(e,t,r)=>{const a=await p(e),n=Date.now();await a.put(e+"_1",Object.assign(r,{__timestamp:n}),t),a.close()};self.onmessage=async function(e){const t={apiKey:e.data.token,basePath:e.data.basePath},r=new(n())(t),a=e.data.levelRecord.dimensions[e.data.levelRecord.axes.indexOf("X")],s=e.data.levelRecord.dimensions[e.data.levelRecord.axes.indexOf("Y")],l=e.data.levelRecord.downsample,d=e.data.index.x,g=e.data.index.y,p=e.data.tileSize,b=e.data.attribute.type.toLowerCase(),v=e.data.levelRecord.axesMapping,A=new c(e.data.levelRecord.arrayAxes.map((t=>e.data.levelRecord.axesMapping.get(t))).flat(),["C","Y","X"]),x=new Array(A.baseAxes.length);for(let e=0;e<A.baseAxes.length;++e){const t=A.baseAxes[e];x[e]="X"===t||"Y"===t?l:1}const E=new Map,_=[];for(let t=0;t<=e.data.channelRanges.length;t+=2)for(let r=e.data.channelRanges[t];r<=e.data.channelRanges[t+1];++r){const t=await y(`${e.data.levelRecord.id}_${p}`,`${r}_${e.data.levelRecord.zoomLevel}_${d}_${g}`);t?E.set(r,t):_.push(r)}const R=new Map;R.set("Y",[g*p*l,Math.min((g+1)*p*l,s)-1]),R.set("X",[d*p*l,Math.min((d+1)*p*l,a)-1]);const w=~~((R.get("X")[1]-R.get("X")[0]+1)/l),S=~~((R.get("Y")[1]-R.get("Y")[0]+1)/l);if(R.get("X")[1]=R.get("X")[0]+w*l-1,R.get("Y")[1]=R.get("Y")[0]+S*l-1,0!==_.length){const t=[];for(const[e,r]of _.entries())0===t.length?t.push(r):r-_[e-1]!=1&&t.push(_[e-1],r);t.push(_.at(-1)),R.set("C",t);const a=function(e,t,r,a,n,o){const s=[];for(const l of r){const i=a.get(l);if(1===i.length)s.push(f(n.get(i[0])));else{const a=[];for(const r of i)a.push(e[t.indexOf(r)]);const c=new Array(i.length).fill(1);for(let e=0;e<a.length;++e)for(let t=e+1;t<a.length;++t)c[e]*=a[t];const f=[],d=[];for(const e of i){const t=[],r=[],a=n.get(e);for(let e=0;e<a.length;e+=2)t.push(a[e+1]-a[e]+1),r.push(a[e]);f.push(t),d.push(r)}const g=u(...f),p=u(...d),y=[],m=[];for(const e of p){let t=0;for(let r=0;r<e.length;++r)t+=e[r]*c[r];y.push(t)}for(const e of g){const t=new Array(i.length+1).fill(Number.MAX_SAFE_INTEGER,0,1).fill(1,1);for(let r=0;r<e.length;++r)for(let a=r+1;a<e.length;++a)t[r+1]*=e[a];m.push(t)}let b=0;const v=new Array(i.length),A=[],x=o[r.indexOf(l)];for(let e=0;e<g.length;++e){const t=g[e].reduce(((e,t)=>e*t),1);for(let r=0;r<t;++r){b=y[e];for(let t=0;t<m[e].length-1;++t)v[t]=~~(r%m[e][t]/m[e][t+1]),b+=v[t]*c[t];if(b>=x)return console.error("OOB"),[];A.push(b)}}A.sort(((e,t)=>e-t)),s.push(h(A))}}return s}(e.data.levelRecord.dimensions,e.data.levelRecord.axes,e.data.levelRecord.arrayAxes,v,R,e.data.levelRecord.arrayExtends);if(0===a.length)return;const n={layout:o.Layout.RowMajor,ranges:a,bufferSize:12e7,attributes:[e.data.attribute.name],returnRawBuffers:!0},s=r.query.ReadQuery(e.data.namespace,e.data.levelRecord.id,n),l=i[b].create(await s.next().then((t=>t.value[e.data.attribute.name]))),c=[];for(const t of e.data.levelRecord.arrayAxes)for(const r of e.data.levelRecord.axesMapping.get(t).flat())switch(r){case"X":case"Y":c.push(R.get(r)[1]-R.get(r)[0]+1);break;case"C":c.push(_.length)}const y=function(e,t,r,a){if(t.baseAxes.toString()===t.targetAxes.toString()&&1===Math.max(...a))return e;const n=t.reshape(r),o=t.reshape(a);let s=1;for(let e=0;e<n.length;++e)n[e]=~~(n[e]/o[e]),s*=n[e];const l=new e.constructor(s),i=new Array(t.baseAxes.length+1).fill(Number.MAX_SAFE_INTEGER,0,1).fill(1,1),c=new Array(t.baseAxes.length).fill(1);for(let e=0;e<r.length;++e)for(let t=e+1;t<r.length;++t)i[e+1]*=r[t],c[e]*=n[t];let f=0;const u=a.reduce(((e,t)=>e*t),1),h=new Array(t.baseAxes.length);for(let r=0;r<e.length;++r){f=0;for(let e=0;e<i.length-1;++e)h[e]=~~(r%i[e]/i[e+1]),f+=~~(h[e]/o[t.permutationMatrix[e]])*c[t.permutationMatrix[e]];l[f]+=e[r]/u}return l}(l,A,c,x);for(const[t,r]of _.entries()){const a=y.slice(t*w*S,(t+1)*w*S);E.set(r,a),await m(`${e.data.levelRecord.id}_${p}`,`${r}_${e.data.levelRecord.zoomLevel}_${d}_${g}`,a)}}const T=i[b].create(E.size*w*S);let O=0;for(let t=0;t<=e.data.channelRanges.length;t+=2)for(let r=e.data.channelRanges[t];r<=e.data.channelRanges[t+1];++r)T.set(E.get(r),O*w*S),++O;self.postMessage({data:T,width:w,height:S,channels:E.size},[T.buffer])}},8291:()=>{},4447:()=>{}},a={};function n(e){var t=a[e];if(void 0!==t)return t.exports;var o=a[e]={exports:{}};return r[e].call(o.exports,o,o.exports,n),o.exports}n.m=r,n.c=a,n.x=()=>{var e=n.O(void 0,[995],(()=>n(3281)));return n.O(e)},e=[],n.O=(t,r,a,o)=>{if(!r){var s=1/0;for(f=0;f<e.length;f++){for(var[r,a,o]=e[f],l=!0,i=0;i<r.length;i++)(!1&o||s>=o)&&Object.keys(n.O).every((e=>n.O[e](r[i])))?r.splice(i--,1):(l=!1,o<s&&(s=o));if(l){e.splice(f--,1);var c=a();void 0!==c&&(t=c)}}return t}o=o||0;for(var f=e.length;f>0&&e[f-1][2]>o;f--)e[f]=e[f-1];e[f]=[r,a,o]},n.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return n.d(t,{a:t}),t},n.d=(e,t)=>{for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},n.f={},n.e=e=>Promise.all(Object.keys(n.f).reduce(((t,r)=>(n.f[r](e,t),t)),[])),n.u=e=>e+".ed09fb94a4cde32b3298.js?v=ed09fb94a4cde32b3298",n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),n.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{n.S={};var e={},t={};n.I=(r,a)=>{a||(a=[]);var o=t[r];if(o||(o=t[r]={}),!(a.indexOf(o)>=0)){if(a.push(o),e[r])return e[r];n.o(n.S,r)||(n.S[r]={}),n.S[r];var s=[];return e[r]=s.length?Promise.all(s).then((()=>e[r]=1)):1}}})(),(()=>{var e;n.g.importScripts&&(e=n.g.location+"");var t=n.g.document;if(!e&&t&&(t.currentScript&&(e=t.currentScript.src),!e)){var r=t.getElementsByTagName("script");if(r.length)for(var a=r.length-1;a>-1&&!e;)e=r[a--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),n.p=e})(),(()=>{var e={79:1};n.f.i=(t,r)=>{e[t]||importScripts(n.p+n.u(t))};var t=self.webpackChunk_tiledb_inc_jupyter_bioimage_viewer=self.webpackChunk_tiledb_inc_jupyter_bioimage_viewer||[],r=t.push.bind(t);t.push=t=>{var[a,o,s]=t;for(var l in o)n.o(o,l)&&(n.m[l]=o[l]);for(s&&s(n);a.length;)e[a.pop()]=1;r(t)}})(),t=n.x,n.x=()=>n.e(995).then(t),n.x()})();