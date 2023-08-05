"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3],{6222:function(e,r,t){t.d(r,{U:function(){return e3}});var o=t(7294),n=t(4761),a=t(4526),i=t(1986),l=t(6289),c=t(5851),s=t(542);let d={context:"Accordion component was not found in the tree",itemContext:"Accordion.Item component was not found in the tree",value:"Accordion.Item component was rendered with invalid value or without value"},[f,u]=(0,s.R)(d.context);function p({children:e,multiple:r,value:t,defaultValue:n,onChange:a,id:s,loop:u,transitionDuration:p,disableChevronRotation:m,chevronPosition:b,chevronSize:v,order:y,chevron:g,variant:h,radius:w}){let O=(0,l.M)(s),[x,P]=(0,c.C)({value:t,defaultValue:n,finalValue:r?[]:null,onChange:a}),k=e=>Array.isArray(x)?x.includes(e):e===x,j=e=>{let r=Array.isArray(x)?x.includes(e)?x.filter(r=>r!==e):[...x,e]:e===x?null:e;P(r)};return o.createElement(f,{value:{isItemActive:k,onChange:j,getControlId:(0,i.A)(`${O}-control`,d.value),getRegionId:(0,i.A)(`${O}-panel`,d.value),transitionDuration:p,disableChevronRotation:m,chevronPosition:b,chevronSize:v,order:y,chevron:g,loop:u,variant:h,radius:w}},e)}let[m,b]=(0,s.R)(d.itemContext);var v=t(6817),y=(0,v.k)((e,r)=>({item:function(e,{variant:r,radius:t}){let o="dark"===e.colorScheme?e.colors.dark[4]:e.colors.gray[3],n="dark"===e.colorScheme?e.colors.dark[6]:e.colors.gray[0],a=e.fn.radius(t);return"default"===r?{color:"dark"===e.colorScheme?e.colors.dark[0]:e.black,borderBottom:`1px solid ${o}`}:"contained"===r?{border:`1px solid ${o}`,transition:"background-color 150ms ease","&[data-active]":{backgroundColor:n},"&:first-of-type":{borderTopRightRadius:a,borderTopLeftRadius:a,"& > [data-accordion-control]":{borderTopRightRadius:a,borderTopLeftRadius:a}},"&:last-of-type":{borderBottomRightRadius:a,borderBottomLeftRadius:a,"& > [data-accordion-control]":{borderBottomRightRadius:a,borderBottomLeftRadius:a}},"& + &":{borderTop:0}}:"filled"===r?{borderRadius:a,"&[data-active]":{backgroundColor:n}}:"separated"===r?{borderRadius:a,backgroundColor:n,border:"1px solid transparent",transition:"background-color 150ms ease","& + &":{marginTop:e.spacing.md},"&[data-active]":{backgroundColor:"dark"===e.colorScheme?e.colors.dark[7]:e.white,borderColor:o}}:{}}(e,r)})),g=t(4523),h=Object.defineProperty,w=Object.getOwnPropertySymbols,O=Object.prototype.hasOwnProperty,x=Object.prototype.propertyIsEnumerable,P=(e,r,t)=>r in e?h(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,k=(e,r)=>{for(var t in r||(r={}))O.call(r,t)&&P(e,t,r[t]);if(w)for(var t of w(r))x.call(r,t)&&P(e,t,r[t]);return e},j=(e,r)=>{var t={};for(var o in e)O.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&w)for(var o of w(e))0>r.indexOf(o)&&x.call(e,o)&&(t[o]=e[o]);return t};let E=(0,o.forwardRef)((e,r)=>{var{children:t,className:n,value:i}=e,l=j(e,["children","className","value"]);let{classNames:c,styles:s,unstyled:d}=(0,a.F)(),f=u(),{classes:p,cx:b}=y({variant:f.variant,radius:f.radius},{name:"Accordion",classNames:c,styles:s,unstyled:d});return o.createElement(m,{value:{value:i}},o.createElement(g.x,k({ref:r,className:b(p.item,n),"data-active":f.isItemActive(i)||void 0},l),t))});E.displayName="@mantine/core/AccordionItem";var C=t(4192),S=Object.defineProperty,N=Object.defineProperties,R=Object.getOwnPropertyDescriptors,I=Object.getOwnPropertySymbols,D=Object.prototype.hasOwnProperty,z=Object.prototype.propertyIsEnumerable,A=(e,r,t)=>r in e?S(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,$=(e,r)=>{for(var t in r||(r={}))D.call(r,t)&&A(e,t,r[t]);if(I)for(var t of I(r))z.call(r,t)&&A(e,t,r[t]);return e},T=(e,r)=>N(e,R(r)),L=(e,r)=>{var t={};for(var o in e)D.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&I)for(var o of I(e))0>r.indexOf(o)&&z.call(e,o)&&(t[o]=e[o]);return t},B=(0,v.k)((e,r)=>{var{transitionDuration:t,chevronPosition:o,chevronSize:n}=r,a=L(r,["transitionDuration","chevronPosition","chevronSize"]);return{icon:{display:"flex",alignItems:"center",justifyContent:"center",marginRight:"left"===o?0:e.spacing.sm,marginLeft:"left"===o?e.spacing.lg:0},chevron:{display:"flex",alignItems:"center",justifyContent:"center",transition:`transform ${t}ms ease`,marginRight:"right"===o?0:e.spacing.sm,marginLeft:"right"===o?e.spacing.lg:0,width:n,minWidth:n,"&[data-rotate]":{transform:"rotate(180deg)"}},label:{color:"inherit",fontWeight:400,flex:1,overflow:"hidden",textOverflow:"ellipsis"},itemTitle:{margin:0,padding:0},control:T($($($({},e.fn.focusStyles()),e.fn.fontStyles()),function(e,{variant:r}){return"default"===r||"contained"===r?e.fn.hover({backgroundColor:"dark"===e.colorScheme?e.colors.dark[6]:e.colors.gray[0]}):{}}(e,a)),{width:"100%",display:"flex",alignItems:"center",flexDirection:"right"===o?"row-reverse":"row",padding:`${e.spacing.md}px ${e.spacing.md/2}px`,paddingLeft:"right"===o?`calc(${e.spacing.sm}px + 4px)`:null,textAlign:"left",color:"dark"===e.colorScheme?e.colors.dark[0]:e.black,"&:disabled":$({opacity:.4,cursor:"not-allowed"},e.fn.hover({backgroundColor:"transparent"}))})}}),F=t(4736),M=Object.defineProperty,G=Object.defineProperties,W=Object.getOwnPropertyDescriptors,H=Object.getOwnPropertySymbols,X=Object.prototype.hasOwnProperty,K=Object.prototype.propertyIsEnumerable,V=(e,r,t)=>r in e?M(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,_=(e,r)=>{for(var t in r||(r={}))X.call(r,t)&&V(e,t,r[t]);if(H)for(var t of H(r))K.call(r,t)&&V(e,t,r[t]);return e},q=(e,r)=>G(e,W(r)),Y=(e,r)=>{var t={};for(var o in e)X.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&H)for(var o of H(e))0>r.indexOf(o)&&K.call(e,o)&&(t[o]=e[o]);return t};let U=(0,o.forwardRef)((e,r)=>{var{disabled:t,onKeyDown:n,onClick:i,chevron:l,children:c,className:s,icon:d}=e,f=Y(e,["disabled","onKeyDown","onClick","chevron","children","className","icon"]);let p=u(),{value:m}=b(),{classNames:v,styles:y,unstyled:g}=(0,a.F)(),{classes:h,cx:w}=B({transitionDuration:p.transitionDuration,chevronPosition:p.chevronPosition,chevronSize:p.chevronSize,variant:p.variant,radius:p.radius},{name:"Accordion",classNames:v,styles:y,unstyled:g}),O=p.isItemActive(m),x="number"==typeof p.order,P=`h${p.order}`,k=o.createElement(F.k,q(_({},f),{ref:r,"data-accordion-control":!0,disabled:t,className:w(h.control,s),onClick(e){null==i||i(e),p.onChange(m)},type:"button","data-active":O||void 0,"aria-expanded":O,"aria-controls":p.getRegionId(m),id:p.getControlId(m),unstyled:g,onKeyDown:(0,C.R)({siblingSelector:"[data-accordion-control]",parentSelector:"[data-accordion]",activateOnFocus:!1,loop:p.loop,orientation:"vertical",onKeyDown:n})}),o.createElement("div",{className:h.chevron,"data-rotate":!p.disableChevronRotation&&O||void 0},l||p.chevron),o.createElement("div",{className:h.label},c),d&&o.createElement("div",{className:h.icon},d));return x?o.createElement(P,{className:h.itemTitle},k):k});U.displayName="@mantine/core/AccordionControl";var Z=Object.defineProperty,J=Object.defineProperties,Q=Object.getOwnPropertyDescriptors,ee=Object.getOwnPropertySymbols,er=Object.prototype.hasOwnProperty,et=Object.prototype.propertyIsEnumerable,eo=(e,r,t)=>r in e?Z(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,en=(e,r)=>{for(var t in r||(r={}))er.call(r,t)&&eo(e,t,r[t]);if(ee)for(var t of ee(r))et.call(r,t)&&eo(e,t,r[t]);return e},ea=(e,r)=>J(e,Q(r)),ei=(0,v.k)((e,r)=>({panel:ea(en({},e.fn.fontStyles()),{wordBreak:"break-word",lineHeight:e.lineHeight}),content:{padding:e.spacing.md,paddingTop:`calc(${e.spacing.xs}px / 2)`}})),el=t(3524),ec=t(3935),es=t(7048),ed=t(4731),ef=Object.defineProperty,eu=Object.defineProperties,ep=Object.getOwnPropertyDescriptors,em=Object.getOwnPropertySymbols,eb=Object.prototype.hasOwnProperty,ev=Object.prototype.propertyIsEnumerable,ey=(e,r,t)=>r in e?ef(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,eg=(e,r)=>{for(var t in r||(r={}))eb.call(r,t)&&ey(e,t,r[t]);if(em)for(var t of em(r))ev.call(r,t)&&ey(e,t,r[t]);return e},eh=(e,r)=>eu(e,ep(r)),ew=(e,r)=>{var t={};for(var o in e)eb.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&em)for(var o of em(e))0>r.indexOf(o)&&ev.call(e,o)&&(t[o]=e[o]);return t};function eO(e){return(null==e?void 0:e.current)?e.current.scrollHeight:"auto"}let ex="undefined"!=typeof window&&window.requestAnimationFrame;var eP=t(2756),ek=Object.defineProperty,ej=Object.getOwnPropertySymbols,eE=Object.prototype.hasOwnProperty,eC=Object.prototype.propertyIsEnumerable,eS=(e,r,t)=>r in e?ek(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,eN=(e,r)=>{for(var t in r||(r={}))eE.call(r,t)&&eS(e,t,r[t]);if(ej)for(var t of ej(r))eC.call(r,t)&&eS(e,t,r[t]);return e},eR=(e,r)=>{var t={};for(var o in e)eE.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&ej)for(var o of ej(e))0>r.indexOf(o)&&eC.call(e,o)&&(t[o]=e[o]);return t};let eI={transitionDuration:200,transitionTimingFunction:"ease",animateOpacity:!0,axis:"y"},eD=(0,o.forwardRef)((e,r)=>{let t=(0,n.N4)("Collapse",eI,e),{children:a,in:i,transitionDuration:l,transitionTimingFunction:c,style:s,onTransitionEnd:d,animateOpacity:f,axis:u}=t,p=eR(t,["children","in","transitionDuration","transitionTimingFunction","style","onTransitionEnd","animateOpacity","axis"]),m=(0,n.rZ)(),b=(0,el.J)(),v=!!m.respectReducedMotion&&b,y=v?0:l,{systemStyles:h,rest:w}=(0,eP.x)(p),O=function({transitionDuration:e,transitionTimingFunction:r="ease",onTransitionEnd:t=()=>{},opened:n,axis:a}){let i=(0,o.useRef)(null),[l,c]=(0,o.useState)({}),s=e=>{(0,ec.flushSync)(()=>c(e))},d=e=>{s(r=>eg(eg({},r),e))};function f(t){let o=e||function(e){if(!e||"string"==typeof e)return 0;let r=e/36;return Math.round((4+15*r**.25+r/5)*10)}(t);return{transitionProperty:`${"x"===a?"width":"height"}`,transitionDuration:`${o}ms`,transitionTimingFunction:`${r}`}}let u=()=>{s({});let e={width:(null==i?void 0:i.current)?i.current.scrollWidth:"auto",height:eO(i)};return s(l),e},p=()=>{let{height:e}=u();return{x:{height:e,width:"0px",overflow:"hidden"},y:{display:"none",height:"0px",overflow:"hidden"}}};(0,o.useEffect)(()=>{ex(()=>{let{x:e,y:r}=p();"x"!==a||n?"y"!==a||n||s(eg({},r)):s(eg({},e))})},[]),(0,es.l)(()=>{"x"!==a&&(n?ex(()=>{d({willChange:"height",display:"block",overflow:"hidden"}),ex(()=>{let e=eO(i);d(eh(eg({},f(e)),{height:e}))})}):ex(()=>{let e=eO(i);d(eh(eg({},f(e)),{willChange:"height",height:e})),ex(()=>d({height:"0px",overflow:"hidden"}))}))},[n]),(0,es.l)(()=>{"y"!==a&&(n?ex(()=>{let{width:e}=u();d({display:"block",overflow:"hidden",willChange:"width",flexShrink:0}),ex(()=>{d(eh(eg({},f(e)),{width:e}))})}):ex(()=>{let{width:e,height:r}=u();d(eh(eg({},f(e)),{flexShrink:0,willChange:"width",width:e,height:r})),ex(()=>d({width:"0px",overflow:"hidden"}))}))},[n]);let m=e=>{if(e.target===i.current&&(e.propertyName,1)){if(t(),n)s({});else{let{x:r,y:o}=p();"x"===a?s(r):s(o)}}};return function(e={}){var{style:r={},refKey:t="ref"}=e,o=ew(e,["style","refKey"]);let a=o[t];return eh(eg({"aria-hidden":!n},o),{[t]:(0,ed.l)(i,a),onTransitionEnd:m,style:eg(eg({boxSizing:"border-box"},r),l)})}}({opened:i,transitionDuration:y,transitionTimingFunction:c,onTransitionEnd:d,axis:u});return 0===y?i?o.createElement(g.x,eN({},w),a):null:o.createElement(g.x,eN({},O(eN(eN({style:s,ref:r},w),h))),o.createElement("div",{style:{opacity:i||!f?1:0,transition:f?`opacity ${y}ms ${c}`:"none"}},a))});eD.displayName="@mantine/core/Collapse";var ez=Object.defineProperty,eA=Object.defineProperties,e$=Object.getOwnPropertyDescriptors,eT=Object.getOwnPropertySymbols,eL=Object.prototype.hasOwnProperty,eB=Object.prototype.propertyIsEnumerable,eF=(e,r,t)=>r in e?ez(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,eM=(e,r)=>{for(var t in r||(r={}))eL.call(r,t)&&eF(e,t,r[t]);if(eT)for(var t of eT(r))eB.call(r,t)&&eF(e,t,r[t]);return e},eG=(e,r)=>eA(e,e$(r)),eW=(e,r)=>{var t={};for(var o in e)eL.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&eT)for(var o of eT(e))0>r.indexOf(o)&&eB.call(e,o)&&(t[o]=e[o]);return t};function eH(e){var{children:r,className:t}=e,n=eW(e,["children","className"]);let i=u(),{value:l}=b(),{classNames:c,styles:s,unstyled:d}=(0,a.F)(),{classes:f,cx:p}=ei({variant:i.variant,radius:i.radius},{name:"Accordion",classNames:c,styles:s,unstyled:d});return o.createElement(eD,eG(eM({},n),{className:p(f.panel,t),in:i.isItemActive(l),transitionDuration:i.transitionDuration,role:"region",id:i.getRegionId(l),"aria-labelledby":i.getControlId(l)}),o.createElement("div",{className:f.content},r))}eH.displayName="@mantine/core/AccordionPanel";var eX=Object.defineProperty,eK=Object.getOwnPropertySymbols,eV=Object.prototype.hasOwnProperty,e_=Object.prototype.propertyIsEnumerable,eq=(e,r,t)=>r in e?eX(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,eY=(e,r)=>{for(var t in r||(r={}))eV.call(r,t)&&eq(e,t,r[t]);if(eK)for(var t of eK(r))e_.call(r,t)&&eq(e,t,r[t]);return e},eU=Object.defineProperty,eZ=Object.defineProperties,eJ=Object.getOwnPropertyDescriptors,eQ=Object.getOwnPropertySymbols,e0=Object.prototype.hasOwnProperty,e1=Object.prototype.propertyIsEnumerable,e5=(e,r,t)=>r in e?eU(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,e4=(e,r)=>{for(var t in r||(r={}))e0.call(r,t)&&e5(e,t,r[t]);if(eQ)for(var t of eQ(r))e1.call(r,t)&&e5(e,t,r[t]);return e},e6=(e,r)=>eZ(e,eJ(r)),e7=(e,r)=>{var t={};for(var o in e)e0.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&eQ)for(var o of eQ(e))0>r.indexOf(o)&&e1.call(e,o)&&(t[o]=e[o]);return t};let e2={multiple:!1,disableChevronRotation:!1,transitionDuration:200,chevronPosition:"right",variant:"default",chevronSize:24,chevron:o.createElement(function(e){return o.createElement("svg",eY({viewBox:"0 0 15 15",fill:"none",xmlns:"http://www.w3.org/2000/svg",width:16,height:16},e),o.createElement("path",{d:"M3.13523 6.15803C3.3241 5.95657 3.64052 5.94637 3.84197 6.13523L7.5 9.56464L11.158 6.13523C11.3595 5.94637 11.6759 5.95657 11.8648 6.15803C12.0536 6.35949 12.0434 6.67591 11.842 6.86477L7.84197 10.6148C7.64964 10.7951 7.35036 10.7951 7.15803 10.6148L3.15803 6.86477C2.95657 6.67591 2.94637 6.35949 3.13523 6.15803Z",fill:"currentColor",fillRule:"evenodd",clipRule:"evenodd"}))},null)};function e3(e){let r=(0,n.N4)("Accordion",e2,e),{id:t,loop:i,children:l,multiple:c,value:s,defaultValue:d,onChange:f,transitionDuration:u,disableChevronRotation:m,chevronPosition:b,chevronSize:v,order:y,chevron:h,classNames:w,styles:O,unstyled:x,variant:P,radius:k}=r,j=e7(r,["id","loop","children","multiple","value","defaultValue","onChange","transitionDuration","disableChevronRotation","chevronPosition","chevronSize","order","chevron","classNames","styles","unstyled","variant","radius"]);return o.createElement(p,{id:t,multiple:c,value:s,defaultValue:d,onChange:f,loop:i,transitionDuration:u,disableChevronRotation:m,chevronPosition:b,chevronSize:v,order:y,chevron:h,variant:P,radius:k},o.createElement(a.V,{classNames:w,styles:O,unstyled:x},o.createElement(g.x,e6(e4({},j),{"data-accordion":!0}),l)))}e3.Item=E,e3.Control=U,e3.Panel=eH,e3.displayName="@mantine/core/Accordion"},4777:function(e,r,t){t.d(r,{i:function(){return x}});var o=t(7294),n=t(4761),a=t(6817);let i={xs:1,sm:2,md:3,lg:4,xl:5};function l(e,r){let t=e.fn.variant({variant:"outline",color:r}).border;return"string"==typeof r&&(r in e.colors||r.split(".")[0]in e.colors)?t:void 0===r?"dark"===e.colorScheme?e.colors.dark[4]:e.colors.gray[4]:r}var c=(0,a.k)((e,{size:r,variant:t,color:o})=>({root:{},withLabel:{borderTop:"0 !important"},left:{"&::before":{display:"none"}},right:{"&::after":{display:"none"}},label:{display:"flex",alignItems:"center","&::before":{content:'""',flex:1,height:1,borderTop:`${e.fn.size({size:r,sizes:i})}px ${t} ${l(e,o)}`,marginRight:e.spacing.xs},"&::after":{content:'""',flex:1,borderTop:`${e.fn.size({size:r,sizes:i})}px ${t} ${l(e,o)}`,marginLeft:e.spacing.xs}},labelDefaultStyles:{color:"dark"===o?e.colors.dark[1]:e.fn.themeColor(o,"dark"===e.colorScheme?5:e.fn.primaryShade(),!1)},horizontal:{border:0,borderTopWidth:e.fn.size({size:r,sizes:i}),borderTopColor:l(e,o),borderTopStyle:t,margin:0},vertical:{border:0,alignSelf:"stretch",height:"auto",borderLeftWidth:e.fn.size({size:r,sizes:i}),borderLeftColor:l(e,o),borderLeftStyle:t}})),s=t(4523),d=t(5117),f=Object.defineProperty,u=Object.defineProperties,p=Object.getOwnPropertyDescriptors,m=Object.getOwnPropertySymbols,b=Object.prototype.hasOwnProperty,v=Object.prototype.propertyIsEnumerable,y=(e,r,t)=>r in e?f(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,g=(e,r)=>{for(var t in r||(r={}))b.call(r,t)&&y(e,t,r[t]);if(m)for(var t of m(r))v.call(r,t)&&y(e,t,r[t]);return e},h=(e,r)=>u(e,p(r)),w=(e,r)=>{var t={};for(var o in e)b.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&m)for(var o of m(e))0>r.indexOf(o)&&v.call(e,o)&&(t[o]=e[o]);return t};let O={orientation:"horizontal",size:"xs",labelPosition:"left",variant:"solid"},x=(0,o.forwardRef)((e,r)=>{let t=(0,n.N4)("Divider",O,e),{className:a,color:i,orientation:l,size:f,label:u,labelPosition:p,labelProps:m,variant:b,styles:v,classNames:y,unstyled:x}=t,P=w(t,["className","color","orientation","size","label","labelPosition","labelProps","variant","styles","classNames","unstyled"]),{classes:k,cx:j}=c({color:i,size:f,variant:b},{classNames:y,styles:v,unstyled:x,name:"Divider"}),E="horizontal"===l,C=!!u&&E,S=!(null==m?void 0:m.color);return o.createElement(s.x,g({ref:r,className:j(k.root,{[k.vertical]:"vertical"===l,[k.horizontal]:E,[k.withLabel]:C},a),role:"separator"},P),C&&o.createElement(d.x,h(g({},m),{size:(null==m?void 0:m.size)||"xs",sx:{marginTop:2},className:j(k.label,k[p],{[k.labelDefaultStyles]:S})}),u))});x.displayName="@mantine/core/Divider"},50:function(e,r,t){t.d(r,{r:function(){return M}});var o=t(7294),n=t(4761);let a=(0,o.createContext)(null),i=a.Provider,l=()=>(0,o.useContext)(a);var c=t(7447),s=t(6817),d=Object.defineProperty,f=Object.getOwnPropertySymbols,u=Object.prototype.hasOwnProperty,p=Object.prototype.propertyIsEnumerable,m=(e,r,t)=>r in e?d(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,b=(e,r)=>{for(var t in r||(r={}))u.call(r,t)&&m(e,t,r[t]);if(f)for(var t of f(r))p.call(r,t)&&m(e,t,r[t]);return e};let v=(e,r)=>"content"===e?"auto":"auto"===e?"0px":e?`${100/(r/e)}%`:void 0,y=(e,r,t)=>t||"auto"===e||"content"===e?"unset":v(e,r),g=(e,r)=>{if(e)return"auto"===e||r?1:0},h=(e,r)=>0===e?0:e?`${100/(r/e)}%`:void 0;var w=(0,s.k)((e,{gutter:r,grow:t,offset:o,offsetXs:n,offsetSm:a,offsetMd:i,offsetLg:l,offsetXl:s,columns:d,span:f,xs:u,sm:p,md:m,lg:w,xl:O,order:x,orderXs:P,orderSm:k,orderMd:j,orderLg:E,orderXl:C})=>({root:b({boxSizing:"border-box",flexGrow:g(f,t),order:x,padding:e.fn.size({size:r,sizes:e.spacing})/2,marginLeft:h(o,d),flexBasis:v(f,d),flexShrink:0,width:"content"===f?"auto":void 0,maxWidth:y(f,d,t)},function({sizes:e,offsets:r,orders:t,theme:o,columns:n,grow:a}){return c.j1.reduce((i,l)=>(i[`@media (min-width: ${o.breakpoints[l]}px)`]={order:t[l],flexBasis:v(e[l],n),flexShrink:0,width:"content"===e[l]?"auto":void 0,maxWidth:y(e[l],n,a),marginLeft:h(r[l],n),flexGrow:g(e[l],a)},i),{})}({sizes:{xs:u,sm:p,md:m,lg:w,xl:O},offsets:{xs:n,sm:a,md:i,lg:l,xl:s},orders:{xs:P,sm:k,md:j,lg:E,xl:C},theme:e,columns:d,grow:t}))})),O=t(4523),x=Object.defineProperty,P=Object.getOwnPropertySymbols,k=Object.prototype.hasOwnProperty,j=Object.prototype.propertyIsEnumerable,E=(e,r,t)=>r in e?x(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,C=(e,r)=>{for(var t in r||(r={}))k.call(r,t)&&E(e,t,r[t]);if(P)for(var t of P(r))j.call(r,t)&&E(e,t,r[t]);return e},S=(e,r)=>{var t={};for(var o in e)k.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&P)for(var o of P(e))0>r.indexOf(o)&&j.call(e,o)&&(t[o]=e[o]);return t};let N={},R=(0,o.forwardRef)((e,r)=>{let t=(0,n.N4)("Grid.Col",N,e),{children:a,span:i,offset:c,offsetXs:s,offsetSm:d,offsetMd:f,offsetLg:u,offsetXl:p,xs:m,sm:b,md:v,lg:y,xl:g,order:h,orderXs:x,orderSm:P,orderMd:k,orderLg:j,orderXl:E,className:R,id:I,unstyled:D}=t,z=S(t,["children","span","offset","offsetXs","offsetSm","offsetMd","offsetLg","offsetXl","xs","sm","md","lg","xl","order","orderXs","orderSm","orderMd","orderLg","orderXl","className","id","unstyled"]),A=l();if(!A)throw Error("[@mantine/core] Grid.Col was used outside of Grid context");let $=i||A.columns,{classes:T,cx:L}=w({gutter:A.gutter,offset:c,offsetXs:s,offsetSm:d,offsetMd:f,offsetLg:u,offsetXl:p,xs:m,sm:b,md:v,lg:y,xl:g,order:h,orderXs:x,orderSm:P,orderMd:k,orderLg:j,orderXl:E,grow:A.grow,columns:A.columns,span:$},{unstyled:D,name:"Col"});return!("auto"===$||"content"===$||"number"==typeof $&&$>0&&$%1==0)||$>A.columns?null:o.createElement(O.x,C({className:L(T.root,R),ref:r},z),a)});R.displayName="@mantine/core/Col";var I=(0,s.k)((e,{justify:r,align:t,gutter:o})=>({root:{margin:-e.fn.size({size:o,sizes:e.spacing})/2,display:"flex",flexWrap:"wrap",justifyContent:r,alignItems:t}})),D=Object.defineProperty,z=Object.getOwnPropertySymbols,A=Object.prototype.hasOwnProperty,$=Object.prototype.propertyIsEnumerable,T=(e,r,t)=>r in e?D(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,L=(e,r)=>{for(var t in r||(r={}))A.call(r,t)&&T(e,t,r[t]);if(z)for(var t of z(r))$.call(r,t)&&T(e,t,r[t]);return e},B=(e,r)=>{var t={};for(var o in e)A.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&z)for(var o of z(e))0>r.indexOf(o)&&$.call(e,o)&&(t[o]=e[o]);return t};let F={gutter:"md",justify:"flex-start",align:"stretch",columns:12},M=(0,o.forwardRef)((e,r)=>{let t=(0,n.N4)("Grid",F,e),{gutter:a,children:l,grow:c,justify:s,align:d,columns:f,className:u,id:p,unstyled:m}=t,b=B(t,["gutter","children","grow","justify","align","columns","className","id","unstyled"]),{classes:v,cx:y}=I({gutter:a,justify:s,align:d},{unstyled:m,name:"Grid"});return o.createElement(i,{value:{gutter:a,grow:c,columns:f}},o.createElement(O.x,L({className:y(v.root,u),ref:r},b),l))});M.Col=R,M.displayName="@mantine/core/Grid"},8090:function(e,r,t){t.d(r,{u:function(){return A}});var o=t(7294),n=t(6289),a=t(5909),i=t(3317),l=t(6362),c=t(3594),s=t(4761),d=t(6817),f=Object.defineProperty,u=Object.getOwnPropertySymbols,p=Object.prototype.hasOwnProperty,m=Object.prototype.propertyIsEnumerable,b=(e,r,t)=>r in e?f(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,v=(e,r)=>{for(var t in r||(r={}))p.call(r,t)&&b(e,t,r[t]);if(u)for(var t of u(r))m.call(r,t)&&b(e,t,r[t]);return e};let y={xs:320,sm:380,md:440,lg:620,xl:780};var g=(0,d.k)((e,{overflow:r,size:t,centered:o,zIndex:n,fullScreen:a})=>({close:{},overlay:{display:a?"none":void 0},root:{position:"fixed",zIndex:n,top:0,left:0,right:0,bottom:0},inner:{position:"absolute",top:0,left:0,right:0,bottom:0,overflowY:"auto",padding:a?0:`${2*e.spacing.xl}px ${e.spacing.md}px`,display:"flex",justifyContent:"center",alignItems:o?"center":"flex-start"},title:{marginRight:e.spacing.md,textOverflow:"ellipsis",display:"block",wordBreak:"break-word"},modal:v({position:"relative",width:a?"100vw":e.fn.size({sizes:y,size:t}),borderRadius:a?0:void 0,outline:0,backgroundColor:"dark"===e.colorScheme?e.colors.dark[7]:e.white,marginTop:o?"auto":void 0,marginBottom:o?"auto":void 0,zIndex:1},a?{position:"absolute",top:0,left:0,right:0,bottom:0,maxHeight:"100vh",overflowY:"auto"}:{}),header:{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:e.spacing.md,marginRight:-9},body:{maxHeight:"inside"===r?"calc(100vh - 185px)":null,overflowY:"inside"===r?"auto":null,wordBreak:"break-word"}})),h=t(3143),w=t(5933),O=t(4523),x=t(7577),P=t(2623),k=t(5117),j=t(971),E=Object.defineProperty,C=Object.getOwnPropertySymbols,S=Object.prototype.hasOwnProperty,N=Object.prototype.propertyIsEnumerable,R=(e,r,t)=>r in e?E(e,r,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[r]=t,I=(e,r)=>{for(var t in r||(r={}))S.call(r,t)&&R(e,t,r[t]);if(C)for(var t of C(r))N.call(r,t)&&R(e,t,r[t]);return e},D=(e,r)=>{var t={};for(var o in e)S.call(e,o)&&0>r.indexOf(o)&&(t[o]=e[o]);if(null!=e&&C)for(var o of C(e))0>r.indexOf(o)&&N.call(e,o)&&(t[o]=e[o]);return t};let z={size:"md",transitionDuration:250,overflow:"outside",padding:"lg",shadow:"lg",closeOnClickOutside:!0,closeOnEscape:!0,trapFocus:!0,withCloseButton:!0,withinPortal:!0,lockScroll:!0,withFocusReturn:!0,overlayBlur:0,zIndex:(0,c.w)("modal"),exitTransitionDuration:0};function A(e){let r=(0,s.N4)("Modal",z,e),{className:t,opened:c,title:d,onClose:f,children:u,withCloseButton:p,overlayOpacity:m,size:b,transitionDuration:v,exitTransitionDuration:y,closeButtonLabel:E,overlayColor:C,overflow:S,transition:N,padding:R,shadow:A,radius:$,id:T,classNames:L,styles:B,closeOnClickOutside:F,trapFocus:M,closeOnEscape:G,centered:W,target:H,withinPortal:X,zIndex:K,overlayBlur:V,transitionTimingFunction:_,fullScreen:q,unstyled:Y,lockScroll:U,withFocusReturn:Z}=r,J=D(r,["className","opened","title","onClose","children","withCloseButton","overlayOpacity","size","transitionDuration","exitTransitionDuration","closeButtonLabel","overlayColor","overflow","transition","padding","shadow","radius","id","classNames","styles","closeOnClickOutside","trapFocus","closeOnEscape","centered","target","withinPortal","zIndex","overlayBlur","transitionTimingFunction","fullScreen","unstyled","lockScroll","withFocusReturn"]),Q=(0,n.M)(T),ee=`${Q}-title`,er=`${Q}-body`,{classes:et,cx:eo,theme:en}=g({size:b,overflow:S,centered:W,zIndex:K,fullScreen:q},{unstyled:Y,classNames:L,styles:B,name:"Modal"}),ea=(0,a.P)(M&&c),ei="number"==typeof m?m:"dark"===en.colorScheme?.85:.75;(0,i.P)(U&&c);let el=e=>{!M&&"Escape"===e.key&&G&&f()};return(0,o.useEffect)(()=>{if(!M)return window.addEventListener("keydown",el),()=>window.removeEventListener("keydown",el)},[M]),(0,l.u)({opened:c,shouldReturnFocus:M&&Z}),o.createElement(h.q,{withinPortal:X,target:H},o.createElement(w.p,{mounted:c,duration:v,exitDuration:y,timingFunction:_,transitions:{modal:{duration:v,transition:N||(q?"fade":"pop")},overlay:{duration:v/2,transition:"fade",timingFunction:"ease"}}},e=>o.createElement(o.Fragment,null,o.createElement(O.x,I({id:Q,className:eo(et.root,t)},J),o.createElement("div",{style:e.overlay},o.createElement(x.a,{className:et.overlay,sx:{position:"fixed"},zIndex:0,blur:V,color:C||("dark"===en.colorScheme?en.colors.dark[9]:en.black),opacity:ei,unstyled:Y})),o.createElement("div",{role:"presentation",className:et.inner,onClick:()=>F&&f(),onKeyDown(e){var r;let t=(null==(r=e.target)?void 0:r.getAttribute("data-mantine-stop-propagation"))!=="true";t&&"Escape"===e.key&&G&&f()},ref:ea},o.createElement(P.X,{className:et.modal,shadow:A,p:R,radius:$,role:"dialog","aria-labelledby":ee,"aria-describedby":er,"aria-modal":!0,tabIndex:-1,style:e.modal,unstyled:Y,onClick:e=>e.stopPropagation()},(d||p)&&o.createElement("div",{className:et.header},o.createElement(k.x,{id:ee,className:et.title},d),p&&o.createElement(j.P,{iconSize:16,onClick:f,"aria-label":E,className:et.close})),o.createElement("div",{id:er,className:et.body},u)))))))}A.displayName="@mantine/core/Modal"},542:function(e,r,t){t.d(r,{R:function(){return n}});var o=t(7294);function n(e){let r=(0,o.createContext)(null),t=()=>{let t=(0,o.useContext)(r);if(null===t)throw Error(e);return t},n=({children:e,value:t})=>o.createElement(r.Provider,{value:t},e);return[n,t]}},4192:function(e,r,t){function o(e,r){let t=e;for(;(t=t.parentElement)&&!t.matches(r););return t}function n({parentSelector:e,siblingSelector:r,onKeyDown:t,loop:n=!0,activateOnFocus:a=!1,dir:i="rtl",orientation:l}){return c=>{var s;null==t||t(c);let d=Array.from((null==(s=o(c.currentTarget,e))?void 0:s.querySelectorAll(r))||[]).filter(r=>o(c.currentTarget,e)===o(r,e)),f=d.findIndex(e=>c.currentTarget===e),u=function(e,r,t){for(let o=e+1;o<r.length;o+=1)if(!r[o].disabled)return o;if(t){for(let n=0;n<r.length;n+=1)if(!r[n].disabled)return n}return e}(f,d,n),p=function(e,r,t){for(let o=e-1;o>=0;o-=1)if(!r[o].disabled)return o;if(t){for(let n=r.length-1;n>-1;n-=1)if(!r[n].disabled)return n}return e}(f,d,n),m="rtl"===i?p:u,b="rtl"===i?u:p;switch(c.key){case"ArrowRight":"horizontal"===l&&(c.stopPropagation(),c.preventDefault(),d[m].focus(),a&&d[m].click());break;case"ArrowLeft":"horizontal"===l&&(c.stopPropagation(),c.preventDefault(),d[b].focus(),a&&d[b].click());break;case"ArrowUp":"vertical"===l&&(c.stopPropagation(),c.preventDefault(),d[p].focus(),a&&d[p].click());break;case"ArrowDown":"vertical"===l&&(c.stopPropagation(),c.preventDefault(),d[u].focus(),a&&d[u].click());break;case"Home":c.stopPropagation(),c.preventDefault(),d[0].disabled||d[0].focus();break;case"End":{c.stopPropagation(),c.preventDefault();let v=d.length-1;d[v].disabled||d[v].focus()}}}}t.d(r,{R:function(){return n}})},1986:function(e,r,t){t.d(r,{A:function(){return o}});function o(e,r){return t=>{if("string"!=typeof t||0===t.trim().length)throw Error(r);return`${e}-${t}`}}},5851:function(e,r,t){t.d(r,{C:function(){return n}});var o=t(7294);function n({value:e,defaultValue:r,finalValue:t,onChange:n=()=>{}}){let[a,i]=(0,o.useState)(void 0!==r?r:t),l=e=>{i(e),null==n||n(e)};return void 0!==e?[e,n,!0]:[a,l,!1]}},4526:function(e,r,t){t.d(r,{F:function(){return i},V:function(){return a}});var o=t(7294);let n=(0,o.createContext)({classNames:{},styles:{},unstyled:!1});function a({children:e,classNames:r,unstyled:t,styles:a,staticSelector:i}){return o.createElement(n.Provider,{value:{classNames:r,styles:a,unstyled:t,staticSelector:i}},e)}function i(){return(0,o.useContext)(n)}}}]);