"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3077],{1210:function(e,n,t){t.d(n,{Z:function(){return I}});var r=t(82394),i=t(21831),o=t(82684),c=t(47999),l=t(49894),u=t(93461),a=t(57384),s=t(41424),d=t(72454),f=t(28598);function p(e,n){var t=e.children;return(0,f.jsx)(d.HS,{ref:n,children:t})}var h=o.forwardRef(p),m=t(32063),b=t(85019),y=t(82531),g=t(66166),v=t(3055),j=t(49125),x=t(91427),O=t(24141);function w(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function S(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?w(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):w(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var I=function(e){var n,t=e.after,r=e.afterHidden,p=e.afterWidth,w=e.afterWidthOverride,I=e.before,k=e.beforeWidth,P=e.breadcrumbs,Z=e.children,_=e.errors,H=e.headerMenuItems,N=e.headerOffset,C=e.mainContainerHeader,z=e.navigationItems,D=e.setErrors,M=e.subheaderChildren,W=e.title,A=e.uuid,E=(0,O.i)().width,B="dashboard_after_width_".concat(A),F="dashboard_before_width_".concat(A),R=(0,o.useRef)(null),T=(0,o.useState)(w?p:(0,x.U2)(B,p)),U=T[0],L=T[1],Q=(0,o.useState)(!1),Y=Q[0],G=Q[1],J=(0,o.useState)(I?Math.max((0,x.U2)(F,k),13*j.iI):null),X=J[0],q=J[1],K=(0,o.useState)(!1),V=K[0],$=K[1],ee=(0,o.useState)(null)[1],ne=y.ZP.projects.list({},{revalidateOnFocus:!1}).data,te=null===ne||void 0===ne?void 0:ne.projects,re=[];P?re.push.apply(re,(0,i.Z)(P)):(null===te||void 0===te?void 0:te.length)>=1&&re.push.apply(re,[{label:function(){var e;return null===(e=te[0])||void 0===e?void 0:e.name},linkProps:{href:"/"}},{bold:!0,label:function(){return W}}]),(0,o.useEffect)((function(){null===R||void 0===R||!R.current||Y||V||null===ee||void 0===ee||ee(R.current.getBoundingClientRect().width)}),[Y,U,V,X,R,ee,E]),(0,o.useEffect)((function(){Y||(0,x.t8)(B,U)}),[r,Y,U,B]),(0,o.useEffect)((function(){V||(0,x.t8)(F,X)}),[V,X,F]);var ie=(0,g.Z)(p);return(0,o.useEffect)((function(){w&&ie!==p&&L(p)}),[w,p,ie]),(0,f.jsxs)(f.Fragment,{children:[(0,f.jsx)(a.Z,{title:W}),(0,f.jsx)(s.Z,{breadcrumbs:re,menuItems:H,project:null===te||void 0===te?void 0:te[0],version:null===te||void 0===te||null===(n=te[0])||void 0===n?void 0:n.version}),(0,f.jsxs)(d.Nk,{children:[0!==(null===z||void 0===z?void 0:z.length)&&(0,f.jsx)(d.lm,{showMore:!0,children:(0,f.jsx)(b.Z,{navigationItems:z,showMore:!0})}),(0,f.jsx)(u.Z,{flex:1,flexDirection:"column",children:(0,f.jsxs)(m.Z,{after:t,afterHeightOffset:v.Mz,afterHidden:r,afterMousedownActive:Y,afterWidth:U,before:I,beforeHeightOffset:v.Mz,beforeMousedownActive:V,beforeWidth:d.k1+(I?X:0),headerOffset:N,hideAfterCompletely:!0,leftOffset:I?d.k1:null,mainContainerHeader:C,mainContainerRef:R,setAfterMousedownActive:G,setAfterWidth:L,setBeforeMousedownActive:$,setBeforeWidth:q,children:[M&&(0,f.jsx)(h,{children:M}),Z]})})]}),_&&(0,f.jsx)(c.Z,{disableClickOutside:!0,isOpen:!0,onClickOutside:function(){return null===D||void 0===D?void 0:D(null)},children:(0,f.jsx)(l.Z,S(S({},_),{},{onClose:function(){return null===D||void 0===D?void 0:D(null)}}))})]})}},2850:function(e,n,t){t.d(n,{M:function(){return c},W:function(){return o}});var r=t(9518),i=t(3055),o=34*t(49125).iI,c=r.default.div.withConfig({displayName:"indexstyle__BeforeStyle",componentId:"sc-12ee2ib-0"})(["min-height:calc(100vh - ","px);"],i.Mz)},79585:function(e,n,t){t.d(n,{DQ:function(){return s},HY:function(){return c},SA:function(){return d},WH:function(){return o},eC:function(){return u},fF:function(){return l},tC:function(){return a}});var r=t(81132),i=t(9736),o="Workspace",c="Preferences",l="Git settings",u="Users",a="Account",s="Profile",d=function(e){var n=e.owner,t=e.roles,d=e.project_access,f=[{linkProps:{href:"/settings/workspace/preferences"},uuid:c}];(n||t===r.No.ADMIN||0!==(2&d))&&f.push({linkProps:{href:"/settings/workspace/users"},uuid:u}),(!(0,i.YB)()||t<=r.No.EDITOR)&&f.push({linkProps:{href:"/settings/workspace/sync-data"},uuid:l});var p=[{items:f,uuid:o}];return(0,i.YB)()?p.concat([{items:[{linkProps:{href:"/settings/account/profile"},uuid:s}],uuid:a}]):p}},30775:function(e,n,t){t.d(n,{Z:function(){return S}});var r=t(1210),i=t(82394),o=t(12691),c=t.n(o),l=t(10919),u=t(86673),a=t(19711),s=t(9518),d=t(23831),f=t(49125),p=t(90880),h=(f.iI,s.default.div.withConfig({displayName:"indexstyle__SectionTitleStyle",componentId:"sc-1y8dyue-0"})(["padding:","px ","px;"],1*f.iI,2.5*f.iI)),m=s.default.div.withConfig({displayName:"indexstyle__ItemStyle",componentId:"sc-1y8dyue-1"})([""," padding:","px ","px;"," ",""],(0,p.eR)(),1.5*f.iI,2.5*f.iI,(function(e){return!e.selected&&"\n    &:hover {\n      background-color: ".concat((e.theme.background||d.Z.background).codeArea,";\n    }\n  ")}),(function(e){return e.selected&&"\n    background-color: ".concat((e.theme.background||d.Z.background).codeTextarea,";\n  ")})),b=t(28598),y=t(82684);function g(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function v(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?g(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):g(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var j=function(e){var n=e.isItemSelected,t=e.sections;return(0,b.jsx)(u.Z,{py:f.Gg,children:null===t||void 0===t?void 0:t.map((function(e){var t=e.items,r=e.title,i=e.uuid;return(0,b.jsxs)(u.Z,{children:[(0,b.jsx)(h,{children:(0,b.jsx)(a.ZP,{bold:!0,muted:!0,small:!0,uppercase:!0,children:r?r():i})}),null===t||void 0===t?void 0:t.map((function(e){var t=e.label,r=e.linkProps,o=e.onClick,u=e.uuid,a=t?t():u,s=(0,b.jsx)(m,{selected:null===n||void 0===n?void 0:n(v(v({},e),{},{uuidWorkspace:i})),children:a});return r?(0,y.createElement)(c(),v(v({},r),{},{key:u,passHref:!0}),(0,b.jsx)(l.Z,{block:!0,noHoverUnderline:!0,noOutline:!0,sameColorAsText:!0,children:s})):(0,b.jsx)(l.Z,{block:!0,noHoverUnderline:!0,noOutline:!0,onClick:o,preventDefault:!0,sameColorAsText:!0,children:s},u)}))]},i)}))})},x=t(2850),O=t(79585),w=t(9736);var S=function(e){var n=e.after,t=e.afterHidden,i=e.children,o=e.uuidItemSelected,c=e.uuidWorkspaceSelected,l=(0,w.PR)()||{};return(0,b.jsx)(r.Z,{after:n,afterHidden:!n||t,afterWidth:n?50*f.iI:0,afterWidthOverride:!0,before:(0,b.jsx)(x.M,{children:(0,b.jsx)(j,{isItemSelected:function(e){var n=e.uuid,t=e.uuidWorkspace;return c===t&&o===n},sections:(0,O.SA)(l)})}),beforeWidth:x.W,title:"Settings",uuid:"settings/index",children:i})}},87372:function(e,n,t){var r,i,o,c,l,u,a,s,d=t(82394),f=t(26304),p=t(26653),h=t(9518),m=t(33591),b=t(23831),y=t(2005),g=t(31012),v=t(19711),j=t(49125),x=t(86673),O=t(28598),w=["children","condensed","inline","level","marketing","spacingBelow"];function S(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function I(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?S(Object(t),!0).forEach((function(n){(0,d.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):S(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var k=(0,h.css)([""," margin:0;"," "," "," "," "," "," "," "," "," "," "," "," ",""],v.IH,(function(e){return e.color&&"\n    color: ".concat(e.color,"\n  ")}),(function(e){return e.yellow&&"\n    color: ".concat((e.theme.accent||b.Z.accent).yellow,";\n  ")}),(function(e){return e.center&&"\n    text-align: center;\n  "}),(function(e){return!e.monospace&&0===Number(e.weightStyle)&&"\n    font-family: ".concat(y.iI,";\n  ")}),(function(e){return!e.monospace&&1===Number(e.weightStyle)&&"\n    font-family: ".concat(y.LX,";\n  ")}),(function(e){return!e.monospace&&2===Number(e.weightStyle)&&"\n    font-family: ".concat(y.LX,";\n  ")}),(function(e){return!e.monospace&&3===Number(e.weightStyle)&&"\n    font-family: ".concat(y.ry,";\n  ")}),(function(e){return!e.monospace&&4===Number(e.weightStyle)&&"\n    font-family: ".concat(y.YC,";\n  ")}),(function(e){return!e.monospace&&5===Number(e.weightStyle)&&"\n    font-family: ".concat(y.nF,";\n  ")}),(function(e){return!e.monospace&&(6===Number(e.weightStyle)||e.bold)&&"\n    font-family: ".concat(y.nF,";\n  ")}),(function(e){return!e.monospace&&7===Number(e.weightStyle)&&"\n    font-family: ".concat(y.nF,";\n  ")}),(function(e){return!e.monospace&&8===Number(e.weightStyle)&&"\n    font-family: ".concat(y.nF,";\n  ")}),(function(e){return e.lineHeightAuto&&"\n    line-height: normal !important;\n  "})),P=h.default.div.withConfig({displayName:"Headline__HeadlineContainerStyle",componentId:"sc-12jzt2e-0"})(["",""],(function(e){return"\n    color: ".concat((e.theme.content||b.Z.content).active,";\n  ")})),Z=h.default.h1.withConfig({displayName:"Headline__H1HeroStyle",componentId:"sc-12jzt2e-1"})([""," font-size:42px;line-height:56px;"," "," ",""],k,m.media.md(r||(r=(0,p.Z)(["\n    ","\n  "])),g.aQ),m.media.lg(i||(i=(0,p.Z)(["\n    ","\n  "])),g.aQ),m.media.xl(o||(o=(0,p.Z)(["\n    ","\n  "])),g.aQ)),_=h.default.h1.withConfig({displayName:"Headline__H1Style",componentId:"sc-12jzt2e-2"})([""," ",""],k,g.MJ),H=h.default.h1.withConfig({displayName:"Headline__H1MarketingStyle",componentId:"sc-12jzt2e-3"})([""," "," "," "," "," ",""],k,m.media.xs(c||(c=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*j.iI,7*j.iI),m.media.sm(l||(l=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*j.iI,7*j.iI),m.media.md(u||(u=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*j.iI,7*j.iI),m.media.lg(a||(a=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*j.iI,7*j.iI),m.media.xl(s||(s=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*j.iI,7*j.iI)),N=h.default.h2.withConfig({displayName:"Headline__H2Style",componentId:"sc-12jzt2e-4"})([""," ",""],k,g.BL),C=h.default.h3.withConfig({displayName:"Headline__H3Style",componentId:"sc-12jzt2e-5"})([""," font-size:24px;line-height:32px;"],k),z=h.default.h4.withConfig({displayName:"Headline__H4Style",componentId:"sc-12jzt2e-6"})([""," font-size:20px;line-height:28px;"],k),D=h.default.h5.withConfig({displayName:"Headline__H5Style",componentId:"sc-12jzt2e-7"})([""," font-size:18px;line-height:26px;"],k),M=h.default.span.withConfig({displayName:"Headline__SpanStyle",componentId:"sc-12jzt2e-8"})([""," "," "," "," ",""],k,(function(e){return 1===e.level&&"\n    ".concat(g.MJ,"\n  ")}),(function(e){return 2===e.level&&"\n    ".concat(g.BL,"\n  ")}),(function(e){return 3===e.level&&"\n    font-size: 24px;\n    line-height: 32px;\n  "}),(function(e){return 4===e.level&&"\n    font-size: 20px;\n    line-height: 28px;\n  "})),W=function(e){var n,t=e.children,r=e.condensed,i=e.inline,o=e.level,c=e.marketing,l=e.spacingBelow,u=(0,f.Z)(e,w);i?n=M:0===Number(o)?n=Z:1===Number(o)?n=c?H:_:2===Number(o)?n=N:3===Number(o)?n=C:4===Number(o)?n=z:5===Number(o)&&(n=D);var a=(0,O.jsxs)(n,I(I({},u),{},{level:o,children:[l&&(0,O.jsx)(x.Z,{mb:r?2:3,children:t}),!l&&t]}));return i?a:(0,O.jsx)(P,{children:a})};W.defaultProps={level:3,weightStyle:6},n.Z=W}}]);