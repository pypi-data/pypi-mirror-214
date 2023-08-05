var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,i,o,a,d,l,u,f,s,c,p,h,v,b,m,g,y={5290:(e,r,t)=>{var n={"./index":()=>t.e(744).then((()=>()=>t(1744))),"./extension":()=>t.e(744).then((()=>()=>t(1744))),"./style":()=>t.e(747).then((()=>()=>t(9747)))},i=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n="default",i=t.S[n];if(i&&i!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>i,init:()=>o})}},w={};function S(e){var r=w[e];if(void 0!==r)return r.exports;var t=w[e]={id:e,loaded:!1,exports:{}};return y[e].call(t.exports,t,t.exports,S),t.loaded=!0,t.exports}S.m=y,S.c=w,S.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return S.d(r,{a:r}),r},S.d=(e,r)=>{for(var t in r)S.o(r,t)&&!S.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},S.f={},S.e=e=>Promise.all(Object.keys(S.f).reduce(((r,t)=>(S.f[t](e,r),r)),[])),S.u=e=>e+"."+{79:"06e38572ee0f6236bd5c",446:"3bf34f45c93ace9c0f28",556:"06e35fefdb145d6110cd",744:"47a5a334c50247fa5daf",747:"433530952542f03ebc71",995:"ed09fb94a4cde32b3298"}[e]+".js?v="+{79:"06e38572ee0f6236bd5c",446:"3bf34f45c93ace9c0f28",556:"06e35fefdb145d6110cd",744:"47a5a334c50247fa5daf",747:"433530952542f03ebc71",995:"ed09fb94a4cde32b3298"}[e],S.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),S.hmd=e=>((e=Object.create(e)).children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),S.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@tiledb-inc/jupyter-bioimage-viewer:",S.l=(t,n,i,o)=>{if(e[t])e[t].push(n);else{var a,d;if(void 0!==i)for(var l=document.getElementsByTagName("script"),u=0;u<l.length;u++){var f=l[u];if(f.getAttribute("src")==t||f.getAttribute("data-webpack")==r+i){a=f;break}}a||(d=!0,(a=document.createElement("script")).charset="utf-8",a.timeout=120,S.nc&&a.setAttribute("nonce",S.nc),a.setAttribute("data-webpack",r+i),a.src=t),e[t]=[n];var s=(r,n)=>{a.onerror=a.onload=null,clearTimeout(c);var i=e[t];if(delete e[t],a.parentNode&&a.parentNode.removeChild(a),i&&i.forEach((e=>e(n))),r)return r(n)},c=setTimeout(s.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=s.bind(null,a.onerror),a.onload=s.bind(null,a.onload),d&&document.head.appendChild(a)}},S.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},S.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{S.S={};var e={},r={};S.I=(t,n)=>{n||(n=[]);var i=r[t];if(i||(i=r[t]={}),!(n.indexOf(i)>=0)){if(n.push(i),e[t])return e[t];S.o(S.S,t)||(S.S[t]={});var o=S.S[t],a="@tiledb-inc/jupyter-bioimage-viewer",d=(e,r,t,n)=>{var i=o[e]=o[e]||{},d=i[r];(!d||!d.loaded&&(!n!=!d.eager?n:a>d.from))&&(i[r]={get:t,from:a,eager:!!n})},l=[];return"default"===t&&(d("@tiledb-inc/bioimage-viewer","0.1.4",(()=>Promise.all([S.e(995),S.e(556),S.e(446)]).then((()=>()=>S(1556))))),d("@tiledb-inc/jupyter-bioimage-viewer","0.1.3",(()=>S.e(744).then((()=>()=>S(1744)))))),e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;S.g.importScripts&&(e=S.g.location+"");var r=S.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");if(t.length)for(var n=t.length-1;n>-1&&!e;)e=t[n--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),S.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var i=e[n],o=(typeof i)[0];if(n>=r.length)return"u"==o;var a=r[n],d=(typeof a)[0];if(o!=d)return"o"==o&&"n"==d||"s"==d||"u"==o;if("o"!=o&&"u"!=o&&i!=a)return i<a;n++}},i=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(d=e[o]))[0]?"-":(n>0?".":"")+(n=2,d);return t}var a=[];for(o=1;o<e.length;o++){var d=e[o];a.push(0===d?"not("+l()+")":1===d?"("+l()+" || "+l()+")":2===d?a.pop()+" "+a.pop():i(d))}return l();function l(){return a.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],i=n<0;i&&(n=-n-1);for(var a=0,d=1,l=!0;;d++,a++){var u,f,s=d<e.length?(typeof e[d])[0]:"";if(a>=r.length||"o"==(f=(typeof(u=r[a]))[0]))return!l||("u"==s?d>n&&!i:""==s!=i);if("u"==f){if(!l||"u"!=s)return!1}else if(l)if(s==f)if(d<=n){if(u!=e[d])return!1}else{if(i?u>e[d]:u<e[d])return!1;u!=e[d]&&(l=!1)}else if("s"!=s&&"n"!=s){if(i||d<=n)return!1;l=!1,d--}else{if(d<=n||f<s!=i)return!1;l=!1}else"s"!=s&&"n"!=s&&(l=!1,d--)}}var c=[],p=c.pop.bind(c);for(a=1;a<e.length;a++){var h=e[a];c.push(1==h?p()|p():2==h?p()&p():h?o(h,r):!p())}return!!p()},a=(e,r)=>{var t=S.S[e];if(!t||!S.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},d=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},l=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+i(n)+")",u=(e,r,t,n)=>{var i=d(e,t);return o(n,i)||s(l(e,t,i,n)),c(e[t][i])},f=(e,r,t)=>{var i=e[r];return(r=Object.keys(i).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&i[r]},s=e=>{"undefined"!=typeof console&&console.warn&&console.warn(e)},c=e=>(e.loaded=1,e.get()),h=(p=e=>function(r,t,n,i){var o=S.I(r);return o&&o.then?o.then(e.bind(e,r,S.S[r],t,n,i)):e(r,S.S[r],t,n,i)})(((e,r,t,n)=>(a(e,t),u(r,0,t,n)))),v=p(((e,r,t,n,i)=>{var o=r&&S.o(r,t)&&f(r,t,n);return o?c(o):i()})),b={},m={1395:()=>h("default","@jupyter-widgets/base",[,[1,6],[1,5],[1,4],[1,3],[1,2],1,1,1,1]),4614:()=>v("default","@tiledb-inc/bioimage-viewer",[2,0,1,4],(()=>Promise.all([S.e(995),S.e(556),S.e(446)]).then((()=>()=>S(1556))))),4456:()=>h("default","react-dom",[1,17,0,1]),6271:()=>h("default","react",[1,17,0,1])},g={446:[4456,6271],744:[1395,4614]},S.f.consumes=(e,r)=>{S.o(g,e)&&g[e].forEach((e=>{if(S.o(b,e))return r.push(b[e]);var t=r=>{b[e]=0,S.m[e]=t=>{delete S.c[e],t.exports=r()}},n=r=>{delete b[e],S.m[e]=t=>{throw delete S.c[e],r}};try{var i=m[e]();i.then?r.push(b[e]=i.then(t).catch(n)):t(i)}catch(e){n(e)}}))},(()=>{S.b=document.baseURI||self.location.href;var e={448:0};S.f.j=(r,t)=>{var n=S.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var i=new Promise(((t,i)=>n=e[r]=[t,i]));t.push(n[2]=i);var o=S.p+S.u(r),a=new Error;S.l(o,(t=>{if(S.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var i=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;a.message="Loading chunk "+r+" failed.\n("+i+": "+o+")",a.name="ChunkLoadError",a.type=i,a.request=o,n[1](a)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,i,[o,a,d]=t,l=0;if(o.some((r=>0!==e[r]))){for(n in a)S.o(a,n)&&(S.m[n]=a[n]);d&&d(S)}for(r&&r(t);l<o.length;l++)i=o[l],S.o(e,i)&&e[i]&&e[i][0](),e[i]=0},t=self.webpackChunk_tiledb_inc_jupyter_bioimage_viewer=self.webpackChunk_tiledb_inc_jupyter_bioimage_viewer||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})(),S.nc=void 0;var j=S(5290);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@tiledb-inc/jupyter-bioimage-viewer"]=j})();