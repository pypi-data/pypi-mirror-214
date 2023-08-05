"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[289],{1017:function(e,t,r){r.d(t,{Z:function(){return j}});var s=r(7294),i=r(4761),n=r(4574),o=r(2623);let a=(0,s.createContext)({padding:0}),l=a.Provider,u=()=>(0,s.useContext)(a).padding;var c=r(6817),h=(0,c.k)((e,{padding:t,withBorder:r,inheritPadding:s})=>{let i=e.fn.size({size:t,sizes:e.spacing}),n=-1*i,o="dark"===e.colorScheme?e.colors.dark[4]:e.colors.gray[3];return{cardSection:{display:"block",marginLeft:n,marginRight:n,paddingLeft:s?i:void 0,paddingRight:s?i:void 0,borderTop:r&&`1px solid ${o}`,borderBottom:r&&`1px solid ${o}`,"& + &":{borderTop:0},"&[data-first]":{marginTop:n,borderTop:0,borderBottom:r&&`1px solid ${o}`},"&[data-last]":{marginBottom:n,borderBottom:0}}}}),d=r(4523),p=Object.defineProperty,f=Object.getOwnPropertySymbols,y=Object.prototype.hasOwnProperty,v=Object.prototype.propertyIsEnumerable,m=(e,t,r)=>t in e?p(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,b=(e,t)=>{for(var r in t||(t={}))y.call(t,r)&&m(e,r,t[r]);if(f)for(var r of f(t))v.call(t,r)&&m(e,r,t[r]);return e},R=(e,t)=>{var r={};for(var s in e)y.call(e,s)&&0>t.indexOf(s)&&(r[s]=e[s]);if(null!=e&&f)for(var s of f(e))0>t.indexOf(s)&&v.call(e,s)&&(r[s]=e[s]);return r};let g=(0,s.forwardRef)((e,t)=>{var{className:r,withBorder:i=!1,inheritPadding:n=!1,unstyled:o}=e,a=R(e,["className","withBorder","inheritPadding","unstyled"]);let{classes:l,cx:c}=h({padding:u(),withBorder:i,inheritPadding:n},{name:"Card",unstyled:o});return s.createElement(d.x,b({className:c(l.cardSection,r),ref:t},a))});g.displayName="@mantine/core/CardSection";let O=(0,n.F)(g);var S=(0,c.k)(e=>({root:{position:"relative",overflow:"hidden",backgroundColor:"dark"===e.colorScheme?e.colors.dark[6]:e.white}})),E=Object.defineProperty,C=Object.getOwnPropertySymbols,w=Object.prototype.hasOwnProperty,I=Object.prototype.propertyIsEnumerable,Q=(e,t,r)=>t in e?E(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,x=(e,t)=>{for(var r in t||(t={}))w.call(t,r)&&Q(e,r,t[r]);if(C)for(var r of C(t))I.call(t,r)&&Q(e,r,t[r]);return e},T=(e,t)=>{var r={};for(var s in e)w.call(e,s)&&0>t.indexOf(s)&&(r[s]=e[s]);if(null!=e&&C)for(var s of C(e))0>t.indexOf(s)&&I.call(e,s)&&(r[s]=e[s]);return r};let P={p:"md"},k=(0,s.forwardRef)((e,t)=>{let r=(0,i.N4)("Card",P,e),{className:n,p:a,radius:u,children:c,unstyled:h}=r,d=T(r,["className","p","radius","children","unstyled"]),{classes:p,cx:f}=S(null,{name:"Card",unstyled:h}),y=s.Children.toArray(c),v=y.map((e,t)=>"object"==typeof e&&e&&"type"in e&&e.type===O?(0,s.cloneElement)(e,{padding:a,"data-first":0===t||void 0,"data-last":t===y.length-1||void 0}):e);return s.createElement(l,{value:{padding:a}},s.createElement(o.X,x({className:f(p.root,n),radius:u,p:a,ref:t},d),v))});k.Section=O,k.displayName="@mantine/core/Card";let j=(0,n.F)(k)},9236:function(e,t,r){r.d(t,{D:function(){return w}});var s=r(7294),i=r(4761),n=r(6817),o=Object.defineProperty,a=Object.defineProperties,l=Object.getOwnPropertyDescriptors,u=Object.getOwnPropertySymbols,c=Object.prototype.hasOwnProperty,h=Object.prototype.propertyIsEnumerable,d=(e,t,r)=>t in e?o(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,p=(e,t)=>{for(var r in t||(t={}))c.call(t,r)&&d(e,r,t[r]);if(u)for(var r of u(t))h.call(t,r)&&d(e,r,t[r]);return e},f=(e,t)=>a(e,l(t)),y=(0,n.k)((e,{element:t,weight:r,size:s,inline:i})=>({root:f(p({},e.fn.fontStyles()),{fontFamily:e.headings.fontFamily,fontWeight:r||e.headings.sizes[t].fontWeight||e.headings.fontWeight,fontSize:void 0!==s?s in e.headings.sizes?e.headings.sizes[s].fontSize:s:e.headings.sizes[t].fontSize,lineHeight:i?1:void 0!==s&&s in e.headings.sizes?e.headings.sizes[s].lineHeight:e.headings.sizes[t].lineHeight,margin:0})})),v=r(5117),m=Object.defineProperty,b=Object.getOwnPropertySymbols,R=Object.prototype.hasOwnProperty,g=Object.prototype.propertyIsEnumerable,O=(e,t,r)=>t in e?m(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,S=(e,t)=>{for(var r in t||(t={}))R.call(t,r)&&O(e,r,t[r]);if(b)for(var r of b(t))g.call(t,r)&&O(e,r,t[r]);return e},E=(e,t)=>{var r={};for(var s in e)R.call(e,s)&&0>t.indexOf(s)&&(r[s]=e[s]);if(null!=e&&b)for(var s of b(e))0>t.indexOf(s)&&g.call(e,s)&&(r[s]=e[s]);return r};let C={order:1},w=(0,s.forwardRef)((e,t)=>{let r=(0,i.N4)("Title",C,e),{className:n,order:o,children:a,unstyled:l,size:u,weight:c,inline:h}=r,d=E(r,["className","order","children","unstyled","size","weight","inline"]),{classes:p,cx:f}=y({element:`h${o}`,weight:c,size:u,inline:h},{name:"Title",unstyled:l});return[1,2,3,4,5,6].includes(o)?s.createElement(v.x,S({component:`h${o}`,ref:t,className:f(p.root,n)},d),a):null});w.displayName="@mantine/core/Title"},3250:function(e,t,r){/**
 * @license React
 * use-sync-external-store-shim.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var s=r(7294),i="function"==typeof Object.is?Object.is:function(e,t){return e===t&&(0!==e||1/e==1/t)||e!=e&&t!=t},n=s.useState,o=s.useEffect,a=s.useLayoutEffect,l=s.useDebugValue;function u(e){var t=e.getSnapshot;e=e.value;try{var r=t();return!i(e,r)}catch(s){return!0}}var c="undefined"==typeof window||void 0===window.document||void 0===window.document.createElement?function(e,t){return t()}:function(e,t){var r=t(),s=n({inst:{value:r,getSnapshot:t}}),i=s[0].inst,c=s[1];return a(function(){i.value=r,i.getSnapshot=t,u(i)&&c({inst:i})},[e,r,t]),o(function(){return u(i)&&c({inst:i}),e(function(){u(i)&&c({inst:i})})},[e]),l(r),r};t.useSyncExternalStore=void 0!==s.useSyncExternalStore?s.useSyncExternalStore:c},1688:function(e,t,r){e.exports=r(3250)},1503:function(e,t,r){let s;r.d(t,{a:function(){return w}});var i=r(2161),n=r(81),o=r(5761),a=r(3989),l=r(2379);class u extends a.l{constructor(e,t){super(),this.client=e,this.options=t,this.trackedProps=new Set,this.selectError=null,this.bindMethods(),this.setOptions(t)}bindMethods(){this.remove=this.remove.bind(this),this.refetch=this.refetch.bind(this)}onSubscribe(){1===this.listeners.length&&(this.currentQuery.addObserver(this),c(this.currentQuery,this.options)&&this.executeFetch(),this.updateTimers())}onUnsubscribe(){this.listeners.length||this.destroy()}shouldFetchOnReconnect(){return h(this.currentQuery,this.options,this.options.refetchOnReconnect)}shouldFetchOnWindowFocus(){return h(this.currentQuery,this.options,this.options.refetchOnWindowFocus)}destroy(){this.listeners=[],this.clearStaleTimeout(),this.clearRefetchInterval(),this.currentQuery.removeObserver(this)}setOptions(e,t){let r=this.options,s=this.currentQuery;if(this.options=this.client.defaultQueryOptions(e),(0,i.VS)(r,this.options)||this.client.getQueryCache().notify({type:"observerOptionsUpdated",query:this.currentQuery,observer:this}),void 0!==this.options.enabled&&"boolean"!=typeof this.options.enabled)throw Error("Expected enabled to be a boolean");this.options.queryKey||(this.options.queryKey=r.queryKey),this.updateQuery();let n=this.hasListeners();n&&d(this.currentQuery,s,this.options,r)&&this.executeFetch(),this.updateResult(t),n&&(this.currentQuery!==s||this.options.enabled!==r.enabled||this.options.staleTime!==r.staleTime)&&this.updateStaleTimeout();let o=this.computeRefetchInterval();n&&(this.currentQuery!==s||this.options.enabled!==r.enabled||o!==this.currentRefetchInterval)&&this.updateRefetchInterval(o)}getOptimisticResult(e){let t=this.client.getQueryCache().build(this.client,e);return this.createResult(t,e)}getCurrentResult(){return this.currentResult}trackResult(e){let t={};return Object.keys(e).forEach(r=>{Object.defineProperty(t,r,{configurable:!1,enumerable:!0,get:()=>(this.trackedProps.add(r),e[r])})}),t}getCurrentQuery(){return this.currentQuery}remove(){this.client.getQueryCache().remove(this.currentQuery)}refetch({refetchPage:e,...t}={}){return this.fetch({...t,meta:{refetchPage:e}})}fetchOptimistic(e){let t=this.client.defaultQueryOptions(e),r=this.client.getQueryCache().build(this.client,t);return r.isFetchingOptimistic=!0,r.fetch().then(()=>this.createResult(r,t))}fetch(e){var t;return this.executeFetch({...e,cancelRefetch:null==(t=e.cancelRefetch)||t}).then(()=>(this.updateResult(),this.currentResult))}executeFetch(e){this.updateQuery();let t=this.currentQuery.fetch(this.options,e);return null!=e&&e.throwOnError||(t=t.catch(i.ZT)),t}updateStaleTimeout(){if(this.clearStaleTimeout(),i.sk||this.currentResult.isStale||!(0,i.PN)(this.options.staleTime))return;let e=(0,i.Kp)(this.currentResult.dataUpdatedAt,this.options.staleTime);this.staleTimeoutId=setTimeout(()=>{this.currentResult.isStale||this.updateResult()},e+1)}computeRefetchInterval(){var e;return"function"==typeof this.options.refetchInterval?this.options.refetchInterval(this.currentResult.data,this.currentQuery):null!=(e=this.options.refetchInterval)&&e}updateRefetchInterval(e){this.clearRefetchInterval(),this.currentRefetchInterval=e,!i.sk&&!1!==this.options.enabled&&(0,i.PN)(this.currentRefetchInterval)&&0!==this.currentRefetchInterval&&(this.refetchIntervalId=setInterval(()=>{(this.options.refetchIntervalInBackground||o.j.isFocused())&&this.executeFetch()},this.currentRefetchInterval))}updateTimers(){this.updateStaleTimeout(),this.updateRefetchInterval(this.computeRefetchInterval())}clearStaleTimeout(){this.staleTimeoutId&&(clearTimeout(this.staleTimeoutId),this.staleTimeoutId=void 0)}clearRefetchInterval(){this.refetchIntervalId&&(clearInterval(this.refetchIntervalId),this.refetchIntervalId=void 0)}createResult(e,t){let r;let s=this.currentQuery,n=this.options,o=this.currentResult,a=this.currentResultState,u=this.currentResultOptions,h=e!==s,f=h?e.state:this.currentQueryInitialState,y=h?this.currentResult:this.previousQueryResult,{state:v}=e,{dataUpdatedAt:m,error:b,errorUpdatedAt:R,fetchStatus:g,status:O}=v,S=!1,E=!1;if(t._optimisticResults){let C=this.hasListeners(),w=!C&&c(e,t),I=C&&d(e,s,t,n);(w||I)&&(g=(0,l.Kw)(e.options.networkMode)?"fetching":"paused",m||(O="loading")),"isRestoring"===t._optimisticResults&&(g="idle")}if(t.keepPreviousData&&!v.dataUpdatedAt&&null!=y&&y.isSuccess&&"error"!==O)r=y.data,m=y.dataUpdatedAt,O=y.status,S=!0;else if(t.select&&void 0!==v.data){if(o&&v.data===(null==a?void 0:a.data)&&t.select===this.selectFn)r=this.selectResult;else try{this.selectFn=t.select,r=t.select(v.data),r=(0,i.oE)(null==o?void 0:o.data,r,t),this.selectResult=r,this.selectError=null}catch(Q){this.selectError=Q}}else r=v.data;if(void 0!==t.placeholderData&&void 0===r&&"loading"===O){let x;if(null!=o&&o.isPlaceholderData&&t.placeholderData===(null==u?void 0:u.placeholderData))x=o.data;else if(x="function"==typeof t.placeholderData?t.placeholderData():t.placeholderData,t.select&&void 0!==x)try{x=t.select(x),this.selectError=null}catch(T){this.selectError=T}void 0!==x&&(O="success",r=(0,i.oE)(null==o?void 0:o.data,x,t),E=!0)}this.selectError&&(b=this.selectError,r=this.selectResult,R=Date.now(),O="error");let P="fetching"===g,k="loading"===O,j="error"===O,F={status:O,fetchStatus:g,isLoading:k,isSuccess:"success"===O,isError:j,isInitialLoading:k&&P,data:r,dataUpdatedAt:m,error:b,errorUpdatedAt:R,failureCount:v.fetchFailureCount,failureReason:v.fetchFailureReason,errorUpdateCount:v.errorUpdateCount,isFetched:v.dataUpdateCount>0||v.errorUpdateCount>0,isFetchedAfterMount:v.dataUpdateCount>f.dataUpdateCount||v.errorUpdateCount>f.errorUpdateCount,isFetching:P,isRefetching:P&&!k,isLoadingError:j&&0===v.dataUpdatedAt,isPaused:"paused"===g,isPlaceholderData:E,isPreviousData:S,isRefetchError:j&&0!==v.dataUpdatedAt,isStale:p(e,t),refetch:this.refetch,remove:this.remove};return F}updateResult(e){let t=this.currentResult,r=this.createResult(this.currentQuery,this.options);if(this.currentResultState=this.currentQuery.state,this.currentResultOptions=this.options,(0,i.VS)(r,t))return;this.currentResult=r;let s={cache:!0};(null==e?void 0:e.listeners)!==!1&&(()=>{if(!t)return!0;let{notifyOnChangeProps:e}=this.options;if("all"===e||!e&&!this.trackedProps.size)return!0;let r=new Set(null!=e?e:this.trackedProps);return this.options.useErrorBoundary&&r.add("error"),Object.keys(this.currentResult).some(e=>{let s=this.currentResult[e]!==t[e];return s&&r.has(e)})})()&&(s.listeners=!0),this.notify({...s,...e})}updateQuery(){let e=this.client.getQueryCache().build(this.client,this.options);if(e===this.currentQuery)return;let t=this.currentQuery;this.currentQuery=e,this.currentQueryInitialState=e.state,this.previousQueryResult=this.currentResult,this.hasListeners()&&(null==t||t.removeObserver(this),e.addObserver(this))}onQueryUpdate(e){let t={};"success"===e.type?t.onSuccess=!e.manual:"error"!==e.type||(0,l.DV)(e.error)||(t.onError=!0),this.updateResult(t),this.hasListeners()&&this.updateTimers()}notify(e){n.V.batch(()=>{var t,r,s,i,n,o,a,l;e.onSuccess?(null==(t=(r=this.options).onSuccess)||t.call(r,this.currentResult.data),null==(s=(i=this.options).onSettled)||s.call(i,this.currentResult.data,null)):e.onError&&(null==(n=(o=this.options).onError)||n.call(o,this.currentResult.error),null==(a=(l=this.options).onSettled)||a.call(l,void 0,this.currentResult.error)),e.listeners&&this.listeners.forEach(e=>{e(this.currentResult)}),e.cache&&this.client.getQueryCache().notify({query:this.currentQuery,type:"observerResultsUpdated"})})}}function c(e,t){return!1!==t.enabled&&!e.state.dataUpdatedAt&&!("error"===e.state.status&&!1===t.retryOnMount)||e.state.dataUpdatedAt>0&&h(e,t,t.refetchOnMount)}function h(e,t,r){if(!1!==t.enabled){let s="function"==typeof r?r(e):r;return"always"===s||!1!==s&&p(e,t)}return!1}function d(e,t,r,s){return!1!==r.enabled&&(e!==t||!1===s.enabled)&&(!r.suspense||"error"!==e.state.status)&&p(e,r)}function p(e,t){return e.isStaleByTime(t.staleTime)}var f=r(7294),y=r(464);let v=f.createContext((s=!1,{clearReset(){s=!1},reset(){s=!0},isReset:()=>s})),m=()=>f.useContext(v);var b=r(5945);let R=f.createContext(!1),g=()=>f.useContext(R);R.Provider;var O=r(4798);let S=(e,t)=>{(e.suspense||e.useErrorBoundary)&&!t.isReset()&&(e.retryOnMount=!1)},E=e=>{f.useEffect(()=>{e.clearReset()},[e])},C=({result:e,errorResetBoundary:t,useErrorBoundary:r,query:s})=>e.isError&&!t.isReset()&&!e.isFetching&&(0,O.L)(r,[e.error,s]);function w(e,t,r){let s=(0,i._v)(e,t,r);return function(e,t){let r=(0,b.NL)({context:e.context}),s=g(),i=m(),o=r.defaultQueryOptions(e);o._optimisticResults=s?"isRestoring":"optimistic",o.onError&&(o.onError=n.V.batchCalls(o.onError)),o.onSuccess&&(o.onSuccess=n.V.batchCalls(o.onSuccess)),o.onSettled&&(o.onSettled=n.V.batchCalls(o.onSettled)),o.suspense&&"number"!=typeof o.staleTime&&(o.staleTime=1e3),S(o,i),E(i);let[a]=f.useState(()=>new t(r,o)),l=a.getOptimisticResult(o);if((0,y.$)(f.useCallback(e=>s?()=>void 0:a.subscribe(n.V.batchCalls(e)),[a,s]),()=>a.getCurrentResult(),()=>a.getCurrentResult()),f.useEffect(()=>{a.setOptions(o,{listeners:!1})},[o,a]),o.suspense&&l.isLoading&&l.isFetching&&!s)throw a.fetchOptimistic(o).then(({data:e})=>{null==o.onSuccess||o.onSuccess(e),null==o.onSettled||o.onSettled(e,null)}).catch(e=>{i.clearReset(),null==o.onError||o.onError(e),null==o.onSettled||o.onSettled(void 0,e)});if(C({result:l,errorResetBoundary:i,useErrorBoundary:o.useErrorBoundary,query:a.getCurrentQuery()}))throw l.error;return o.notifyOnChangeProps?l:a.trackResult(l)}(s,u)}},464:function(e,t,r){r.d(t,{$:function(){return i}});var s=r(1688);let i=s.useSyncExternalStore},4798:function(e,t,r){r.d(t,{L:function(){return s}});function s(e,t){return"function"==typeof e?e(...t):!!e}}}]);