(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9552],{95372:function(e){e.exports=function(e,t,a,i){for(var s=e.length,r=a+(i?1:-1);i?r--:++r<s;)if(t(e[r],r,e))return r;return -1}},56632:function(e,t,a){var i=a(89278),s=a(80068),r=a(50098);e.exports=function(e){return function(t,a,n){var l=Object(t);if(!s(t)){var o=i(a,3);t=r(t),a=function(e){return o(l[e],e,l)}}var c=e(t,a,n);return c>-1?l[o?t[c]:c]:void 0}}},64925:function(e,t,a){var i=a(56632)(a(66259));e.exports=i},66259:function(e,t,a){var i=a(95372),s=a(89278),r=a(47991),n=Math.max;e.exports=function(e,t,a){var l=null==e?0:e.length;if(!l)return -1;var o=null==a?0:r(a);return o<0&&(o=n(l+o,0)),i(e,s(t,3),o)}},94919:function(e,t,a){var i=a(91936),s=1/0;e.exports=function(e){return e?(e=i(e))===s||e===-s?(e<0?-1:1)*17976931348623157e292:e==e?e:0:0===e?e:0}},47991:function(e,t,a){var i=a(94919);e.exports=function(e){var t=i(e),a=t%1;return t==t?a?t-a:t:0}},36848:function(e,t,a){"use strict";a.d(t,{q:function(){return r}});var i=a(24246),s=a(5152);let r=e=>{let{label:t,isDisabled:a,...r}=e;return(0,i.jsx)(s.OK9,{"data-testid":"tab-".concat(t),_selected:{fontWeight:"600",color:"complimentary.500",borderColor:"complimentary.500"},fontSize:r.fontSize,fontWeight:"500",color:"gray.500",isDisabled:a||!1,children:t})};t.Z=e=>{let{data:t,border:a="partial",...n}=e;return(0,i.jsxs)(s.mQc,{colorScheme:"complimentary",...n,children:[(0,i.jsx)(s.tdY,{width:"partial"===a?"max-content":void 0,children:t.map(e=>(0,i.jsx)(r,{label:e.label,isDisabled:e.isDisabled,fontSize:n.fontSize},e.label))}),(0,i.jsx)(s.nPR,{children:t.map(e=>(0,i.jsx)(s.x45,{px:0,"data-testid":"tab-panel-".concat(e.label),children:e.content},e.label))})]})}},11574:function(e,t,a){"use strict";var i=a(24246),s=a(5152),r=a(36848);t.Z=e=>{let{data:t,border:a="partial",borderWidth:n=2,...l}=e;return(0,i.jsx)(s.mQc,{colorScheme:"complimentary",...l,children:(0,i.jsx)(s.tdY,{width:"partial"===a?"max-content":void 0,borderBottomWidth:n,children:t.map(e=>(0,i.jsx)(r.q,{label:e.label,"data-testid":e.label,isDisabled:e.isDisabled,fontSize:l.fontSize},e.label))})})}},87853:function(e,t,a){"use strict";a.d(t,{Q:function(){return s}});var i=a(24246);let s=(0,a(5152).IUT)({displayName:"SparkleIcon",viewBox:"0 0 18 18",path:(0,i.jsx)("path",{fill:"currentColor",d:"M9.53604 15.8107C9.81449 15.8107 10.0158 15.6256 10.0681 15.3471C10.7648 11.6208 11.1324 11.0552 14.8315 10.559C15.1373 10.518 15.3337 10.303 15.3337 10.0245C15.3337 9.74611 15.1373 9.53357 14.8315 9.49254C11.1609 8.99636 10.6349 8.45671 10.0681 4.71568C10.0246 4.42354 9.81449 4.22717 9.53604 4.22717C9.28 4.22717 9.05872 4.41234 9.01768 4.70447C8.34835 8.43318 7.95089 8.99143 4.24063 9.49254C3.94849 9.53357 3.74963 9.74611 3.74963 10.0245C3.74963 10.303 3.94849 10.5155 4.24063 10.559C7.91753 11.0847 8.446 11.5836 9.01768 15.3359C9.04995 15.6256 9.26003 15.8107 9.53604 15.8107ZM3.62366 7.96543C3.82881 7.96543 3.9954 7.81253 4.03397 7.60739C4.40352 5.74358 4.25772 5.75481 6.22471 5.41918C6.44356 5.38938 6.58033 5.21404 6.58033 5.0089C6.58033 4.81497 6.44109 4.63717 6.22471 4.5986C4.26265 4.27148 4.40105 4.26655 4.03397 2.43529C3.9954 2.22768 3.84249 2.06358 3.62366 2.06358C3.41604 2.06358 3.26314 2.21648 3.21335 2.43529C2.84873 4.25179 2.9896 4.25179 1.02259 4.5986C0.814976 4.63963 0.666992 4.81497 0.666992 5.0089C0.666992 5.23894 0.814976 5.38938 1.05241 5.41918C2.98714 5.74249 2.84626 5.73868 3.21335 7.58252C3.26314 7.80132 3.40483 7.96543 3.62366 7.96543ZM8.03377 3.9032C8.17054 3.9032 8.27749 3.80747 8.30485 3.6707C8.5461 2.4508 8.47882 2.4732 9.75105 2.22703C9.89903 2.19969 9.9923 2.09273 9.9923 1.95599C9.9923 1.81922 9.89656 1.71472 9.74858 1.68738C8.46759 1.43874 8.52367 1.43874 8.30485 0.254909C8.27749 0.106937 8.18175 0 8.03377 0C7.897 0 7.80126 0.106939 7.76269 0.257375C7.50393 1.43874 7.60488 1.43874 6.31652 1.68738C6.16851 1.71472 6.08647 1.81922 6.08647 1.95599C6.08647 2.10396 6.16851 2.19723 6.33265 2.22703C7.60488 2.43956 7.50393 2.45079 7.76269 3.64827C7.80126 3.80747 7.897 3.9032 8.03377 3.9032Z"})})},90824:function(e,t,a){"use strict";a.d(t,{V:function(){return s}});var i=a(24246);let s=(0,a(5152).IUT)({displayName:"DatabaseIcon",viewBox:"0 0 12 12",path:(0,i.jsx)("path",{fill:"currentColor",d:"M6 12C4.32222 12 2.90278 11.7417 1.74167 11.225C0.580556 10.7083 0 10.0778 0 9.33333V2.66667C0 1.93333 0.586111 1.30556 1.75833 0.783333C2.93056 0.261111 4.34444 0 6 0C7.65556 0 9.06944 0.261111 10.2417 0.783333C11.4139 1.30556 12 1.93333 12 2.66667V9.33333C12 10.0778 11.4194 10.7083 10.2583 11.225C9.09722 11.7417 7.67778 12 6 12ZM6 4.01667C6.98889 4.01667 7.98333 3.875 8.98333 3.59167C9.98333 3.30833 10.5444 3.00556 10.6667 2.68333C10.5444 2.36111 9.98611 2.05556 8.99167 1.76667C7.99722 1.47778 7 1.33333 6 1.33333C4.98889 1.33333 3.99722 1.475 3.025 1.75833C2.05278 2.04167 1.48889 2.35 1.33333 2.68333C1.48889 3.01667 2.05278 3.32222 3.025 3.6C3.99722 3.87778 4.98889 4.01667 6 4.01667ZM6 7.33333C6.46667 7.33333 6.91667 7.31111 7.35 7.26667C7.78333 7.22222 8.19722 7.15833 8.59167 7.075C8.98611 6.99167 9.35833 6.88889 9.70833 6.76667C10.0583 6.64444 10.3778 6.50556 10.6667 6.35V4.35C10.3778 4.50556 10.0583 4.64444 9.70833 4.76667C9.35833 4.88889 8.98611 4.99167 8.59167 5.075C8.19722 5.15833 7.78333 5.22222 7.35 5.26667C6.91667 5.31111 6.46667 5.33333 6 5.33333C5.53333 5.33333 5.07778 5.31111 4.63333 5.26667C4.18889 5.22222 3.76944 5.15833 3.375 5.075C2.98056 4.99167 2.61111 4.88889 2.26667 4.76667C1.92222 4.64444 1.61111 4.50556 1.33333 4.35V6.35C1.61111 6.50556 1.92222 6.64444 2.26667 6.76667C2.61111 6.88889 2.98056 6.99167 3.375 7.075C3.76944 7.15833 4.18889 7.22222 4.63333 7.26667C5.07778 7.31111 5.53333 7.33333 6 7.33333ZM6 10.6667C6.51111 10.6667 7.03056 10.6278 7.55833 10.55C8.08611 10.4722 8.57222 10.3694 9.01667 10.2417C9.46111 10.1139 9.83333 9.96945 10.1333 9.80833C10.4333 9.64722 10.6111 9.48333 10.6667 9.31667V7.68333C10.3778 7.83889 10.0583 7.97778 9.70833 8.1C9.35833 8.22222 8.98611 8.325 8.59167 8.40833C8.19722 8.49167 7.78333 8.55556 7.35 8.6C6.91667 8.64444 6.46667 8.66667 6 8.66667C5.53333 8.66667 5.07778 8.64444 4.63333 8.6C4.18889 8.55556 3.76944 8.49167 3.375 8.40833C2.98056 8.325 2.61111 8.22222 2.26667 8.1C1.92222 7.97778 1.61111 7.83889 1.33333 7.68333V9.33333C1.38889 9.5 1.56389 9.66111 1.85833 9.81667C2.15278 9.97222 2.52222 10.1139 2.96667 10.2417C3.41111 10.3694 3.9 10.4722 4.43333 10.55C4.96667 10.6278 5.48889 10.6667 6 10.6667Z"})})},62257:function(e,t,a){"use strict";a.d(t,{l:function(){return s}});var i=a(24246);let s=(0,a(5152).IUT)({displayName:"DatasetIcon",viewBox:"0 0 16 16",path:(0,i.jsx)("path",{fill:"currentColor",d:"M2 14V2H14V14H2ZM3.33333 12.6667H12.6667V3.33333H3.33333V12.6667ZM4.66667 7.33333H7.33333V4.66667H4.66667V7.33333ZM8.66667 7.33333H11.3333V4.66667H8.66667V7.33333ZM4.66667 11.3333H7.33333V8.66667H4.66667V11.3333ZM8.66667 11.3333H11.3333V8.66667H8.66667V11.3333Z"})})},60262:function(e,t,a){"use strict";a.d(t,{f:function(){return s}});var i=a(24246);let s=(0,a(5152).IUT)({displayName:"FieldIcon",viewBox:"0 0 16 16",path:(0,i.jsx)("path",{d:"M12.6667 12.6667V10.6667H3.33333V12.6667H12.6667ZM12.6667 9.33333V6.66667H3.33333V9.33333H12.6667ZM12.6667 5.33333V3.33333H3.33333V5.33333H12.6667ZM3.33333 14C2.96667 14 2.65278 13.8694 2.39167 13.6083C2.13056 13.3472 2 13.0333 2 12.6667V3.33333C2 2.96667 2.13056 2.65278 2.39167 2.39167C2.65278 2.13056 2.96667 2 3.33333 2H12.6667C13.0333 2 13.3472 2.13056 13.6083 2.39167C13.8694 2.65278 14 2.96667 14 3.33333V12.6667C14 13.0333 13.8694 13.3472 13.6083 13.6083C13.3472 13.8694 13.0333 14 12.6667 14H3.33333Z",fill:"currentColor"})})},29137:function(e,t,a){"use strict";a.d(t,{$:function(){return s}});var i=a(24246);let s=(0,a(5152).IUT)({displayName:"TableIcon",viewBox:"0 0 16 16",path:(0,i.jsx)("path",{fill:"currentColor",d:"M2 14V2H14V14H2ZM3.33333 6H12.6667V3.33333H3.33333V6ZM6.88333 9.33333H9.11667V7.33333H6.88333V9.33333ZM6.88333 12.6667H9.11667V10.6667H6.88333V12.6667ZM3.33333 9.33333H5.55V7.33333H3.33333V9.33333ZM10.45 9.33333H12.6667V7.33333H10.45V9.33333ZM3.33333 12.6667H5.55V10.6667H3.33333V12.6667ZM10.45 12.6667H12.6667V10.6667H10.45V12.6667Z"})})},74588:function(e,t,a){"use strict";a.d(t,{l:function(){return c}});var i=a(24246),s=a(5152),r=a(19310),n=a(55372),l=a.n(n);let o=e=>{let{data:t}=e;return(0,i.jsxs)(s.jqI,{gap:12,title:"".concat(t.primaryName||"").concat(t.primaryName?": ":"").concat(t.name," - ").concat(t.description),children:[(0,i.jsxs)("div",{children:[(0,i.jsx)("strong",{children:t.primaryName||t.name}),t.primaryName&&": ".concat(t.name)]}),(0,i.jsx)("em",{children:t.description})]})},c=e=>{let{selectedTaxonomies:t,showDisabled:a=!1,...n}=e,{getDataCategoryDisplayNameProps:c,getDataCategories:d}=(0,r.Z)(),u=(a?d():d().filter(e=>e.active)).filter(e=>!t.includes(e.fides_key)).map(e=>{let{name:t,primaryName:a}=c(e.fides_key);return{value:e.fides_key,name:t,primaryName:a,description:e.description||"",className:l().option}});return(0,i.jsx)(s.WPr,{autoFocus:!0,showSearch:!0,variant:"borderless",placeholder:"Select a category...",options:u,optionRender:o,dropdownStyle:{minWidth:"500px"},className:"w-full p-0","data-testid":"taxonomy-select",...n})}},19310:function(e,t,a){"use strict";var i=a(24246),s=a(64925),r=a.n(s),n=a(27378),l=a(44296),o=a(91650),c=a(79851),d=a(47411);let u=()=>{let{isLoading:e}=(0,c.fd)(),t=(0,l.C)(c.U3),{isLoading:a}=(0,d.MO)(),i=(0,l.C)(d.qb),{isLoading:s}=(0,o.te)();return{dataUses:t,dataSubjects:(0,l.C)(o.ZL),dataCategories:i,isLoading:e||a||s}};t.Z=()=>{let{dataUses:e,dataCategories:t,dataSubjects:a,isLoading:s}=u(),l=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:1;return e.split(".").slice(0,t).join(".")},o=function(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1,i=t(e);if(!i)return{};let s=t(l(e,a)),r=!!i.parent_key;return{name:i.name||void 0,primaryName:r&&(null==s?void 0:s.name)!==i.name&&(null==s?void 0:s.name)||void 0}},c=function(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1,{name:s,primaryName:r}=o(e,t,a);return s?r?(0,i.jsxs)(n.Fragment,{children:[(0,i.jsxs)("strong",{children:[r,":"]})," ",s]},e):(0,i.jsx)("strong",{children:s},e):e},d=t=>r()(e,{fides_key:t}),x=e=>r()(t,{fides_key:e}),g=e=>r()(a,{fides_key:e});return{getDataUses:()=>e,getDataUseByKey:d,getDataUseDisplayName:e=>c(e,d,1),getDataCategories:()=>t,getDataCategoryByKey:x,getDataCategoryDisplayName:e=>c(e,x,2),getDataCategoryDisplayNameProps:e=>o(e,x,2),getDataSubjects:()=>a,getDataSubjectByKey:g,getDataSubjectDisplayName:e=>{let t=g(e);return t?t.name:e},getPrimaryKey:l,isLoading:s}}},76552:function(e,t,a){"use strict";var i=a(24246),s=a(11574);t.Z=e=>{let{filterTabs:t,onChange:a,filterTabIndex:r}=e;return(0,i.jsx)(s.Z,{border:"full-width",mb:5,size:"sm",data:t,borderWidth:1,index:r,onChange:a})}},8339:function(e,t,a){"use strict";var i=a(24246),s=a(5152),r=a(86677),n=a(90824),l=a(62257),o=a(60262),c=a(29137);let d=[(0,i.jsx)(n.V,{boxSize:4},"database"),(0,i.jsx)(l.l,{boxSize:5},"dataset"),(0,i.jsx)(c.$,{boxSize:5},"table"),(0,i.jsx)(o.f,{boxSize:5},"field")];t.Z=e=>{let{resourceUrn:t,parentLink:a,onPathClick:n=()=>{}}=e,l=(0,r.useRouter)();if(!t)return(0,i.jsx)(s.aGc,{separator:"/","data-testid":"results-breadcrumb",fontSize:"sm",fontWeight:"semibold",mt:-1,mb:0,children:(0,i.jsxs)(s.gN6,{children:[d[0],(0,i.jsx)(s.Atw,{ml:1,children:"All activity"})]})});let o=t.split(".");return(0,i.jsx)(s.aGc,{separator:"/","data-testid":"results-breadcrumb",fontSize:"sm",fontWeight:"normal",mt:-1,mb:0,children:o.map((e,t)=>{if(0===t)return null;let r=1===t,c=t===o.length-1;return(0,i.jsxs)(s.gN6,{fontWeight:c?"semibold":"normal",color:c?"gray.800":"gray.500",children:[d[t-1],(0,i.jsx)(s.Atw,{ml:1,onClick:()=>r?l.push(a):n(o.slice(0,t+1).join(".")),children:e})]},e)})})}},27325:function(e,t,a){"use strict";a.d(t,{Z:function(){return U}});var i,s,r=a(24246),n=a(59003),l=a(92222),o=a(5152),c=a(86677),d=a(27378),u=a(8540),x=a(76552),g=a(6111),C=a(98320),m=a(61934),h=a(20382),f=a(51557),p=a(59104),j=a(15025),v=a(10284),b=a(33890),y=a(74588),I=a(19310),_=a(87853),S=e=>{let{children:t,onClick:a,...i}=e;return(0,r.jsx)(o.kCb,{fontSize:"xs",alignItems:"center",gap:1.5,px:1.5,h:"20px",borderWidth:"1px",borderColor:"gray.200",borderRadius:"sm",cursor:a?"pointer":"default",_hover:a?{bg:"gray.100"}:void 0,onClick:a,...i,children:t})};let w=e=>(0,r.jsx)(o.wpx,{size:"small",icon:(0,r.jsx)(o.jBn,{mb:"1px"}),className:" max-h-[20px] max-w-[20px] rounded-sm border-gray-200 bg-white hover:!bg-gray-100","data-testid":"add-category-btn","aria-label":"Add category",...e});var L=e=>{var t,a,i;let{resource:s}=e,[n,l]=(0,d.useState)(!1),{getDataCategoryDisplayName:c}=(0,I.Z)(),[u]=(0,g.NA)(),x=(null===(t=s.classifications)||void 0===t?void 0:t.length)?s.classifications[0].label:null,C=null!==(i=s.user_assigned_data_categories)&&void 0!==i?i:[],m=!x&&!(null==C?void 0:C.length),h=null===(a=s.sub_field_urns)||void 0===a?void 0:a.length,f=e=>{u({staged_resource_urn:s.urn,monitor_config_id:s.monitor_config_id,user_assigned_data_categories:[...C,e]})},p=e=>{var t;u({staged_resource_urn:s.urn,monitor_config_id:s.monitor_config_id,user_assigned_data_categories:null!==(t=null==C?void 0:C.filter(t=>t!==e))&&void 0!==t?t:[]})},j=!n&&!!C.length,v=!n&&!!x&&!C.length;return(0,r.jsxs)(o.Eq9,{py:2,alignItems:"center",position:"relative",width:"100%",gap:2,overflowX:"auto",children:[m&&(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(S,{"data-testid":"no-classifications",children:"None"}),!h&&(0,r.jsx)(w,{onClick:()=>l(!0)})]}),j&&(0,r.jsxs)(r.Fragment,{children:[C.map(e=>(0,r.jsxs)(S,{classification:c(e),"data-testid":"user-classification-".concat(e),children:[c(e),(0,r.jsx)(o.wpx,{onClick:()=>p(e),icon:(0,r.jsx)(o.Two,{boxSize:2,mt:-.5}),size:"small",type:"text",className:"ml-1 max-h-4 max-w-4","aria-label":"Remove category"})]},e)),(0,r.jsx)(w,{onClick:()=>l(!0)})]}),v&&(0,r.jsxs)(S,{onClick:()=>l(!0),cursor:"pointer","data-testid":"classification-".concat(x),children:[(0,r.jsx)(_.Q,{mt:.5}),c(x),(0,r.jsx)(o.dY8,{})]}),n&&(0,r.jsx)(o.xuv,{className:"select-wrapper",position:"absolute",zIndex:10,top:"0",left:"0",width:"100%",height:"max",bgColor:"#fff",children:(0,r.jsx)(y.l,{selectedTaxonomies:C,onChange:e=>{l(!1),f(e)},onBlur:()=>l(!1),open:!0})})]})},Z=a(83135),T=e=>{let{resourceType:t}=e,a=(0,l.Cl)();return t===p.X.SCHEMA?{columns:[a.accessor(e=>e.name,{id:"name",cell:e=>(0,r.jsx)(Z.Z,{result:e.row.original,changeTypeOverride:f.E.CLASSIFICATION}),header:e=>(0,r.jsx)(u.Rr,{value:"Name",...e})}),a.accessor(e=>e.urn,{id:"project",cell:e=>(0,r.jsx)(u.G3,{value:(0,j.Z)(e.getValue())}),header:e=>(0,r.jsx)(u.Rr,{value:"Project",...e})}),a.display({id:"status",cell:e=>(0,r.jsx)(h.Z,{result:e.row.original}),header:e=>(0,r.jsx)(u.Rr,{value:"Status",...e})}),a.accessor(e=>e.system,{id:"system",cell:e=>(0,r.jsx)(u.G3,{value:e.getValue()}),header:e=>(0,r.jsx)(u.Rr,{value:"System",...e})}),a.accessor(e=>e.monitor_config_id,{id:"monitor",cell:e=>(0,r.jsx)(u.G3,{value:e.getValue()}),header:e=>(0,r.jsx)(u.Rr,{value:"Detected by",...e})}),a.accessor(e=>e.updated_at,{id:"time",cell:e=>(0,r.jsx)(C.Cy,{time:e.getValue()}),header:e=>(0,r.jsx)(u.Rr,{value:"When",...e})}),a.display({id:"action",cell:e=>e.row.original.diff_status!==v.LL.MUTED?(0,r.jsx)(b.Z,{resource:e.row.original}):(0,r.jsx)(u.G3,{value:"--"}),header:"Actions",size:180})]}:t===p.X.TABLE?{columns:[a.display({id:"select",cell:e=>{var t;let{row:a}=e;return(0,r.jsx)(C.k,{isChecked:a.getIsSelected(),onChange:a.getToggleSelectedHandler(),dataTestId:"select-".concat(null!==(t=a.original.name)&&void 0!==t?t:a.id)})},header:e=>{let{table:t}=e;return(0,r.jsx)(C.k,{isChecked:t.getIsAllPageRowsSelected(),isIndeterminate:t.getIsSomeRowsSelected(),onChange:t.getToggleAllRowsSelectedHandler(),dataTestId:"select-all-rows"})},maxSize:25}),a.accessor(e=>e.name,{id:"tables",cell:e=>(0,r.jsx)(Z.Z,{result:e.row.original}),header:e=>(0,r.jsx)(u.Rr,{value:"Table name",...e})}),a.accessor(e=>e.description,{id:"description",cell:e=>(0,r.jsx)(u.G3,{value:e.getValue(),cellProps:e}),header:e=>(0,r.jsx)(u.Rr,{value:"Description",...e}),meta:{showHeaderMenu:!0}}),a.display({id:"status",cell:e=>(0,r.jsx)(h.Z,{result:e.row.original}),header:e=>(0,r.jsx)(u.Rr,{value:"Status",...e})}),a.display({id:"type",cell:()=>(0,r.jsx)(u.G3,{value:"Table"}),header:"Type"}),a.accessor(e=>e.updated_at,{id:"time",cell:e=>(0,r.jsx)(C.Cy,{time:e.getValue()}),header:"Time"}),a.display({id:"actions",cell:e=>(0,r.jsx)(b.Z,{resource:e.row.original}),header:"Actions"})]}:t===p.X.FIELD?{columns:[a.accessor(e=>e.name,{id:"name",cell:e=>(0,r.jsx)(Z.Z,{result:e.row.original}),header:e=>(0,r.jsx)(u.Rr,{value:"Field name",...e})}),a.accessor(e=>e.source_data_type,{id:"data-type",cell:e=>(0,r.jsx)(m.Z,{type:e.getValue()}),header:e=>(0,r.jsx)(u.Rr,{value:"Data type",...e})}),a.accessor(e=>e.description,{id:"description",cell:e=>(0,r.jsx)(u.G3,{value:e.getValue(),cellProps:e}),header:e=>(0,r.jsx)(u.Rr,{value:"Description",...e}),meta:{showHeaderMenu:!0}}),a.display({id:"status",cell:e=>(0,r.jsx)(h.Z,{result:e.row.original}),header:e=>(0,r.jsx)(u.Rr,{value:"Status",...e})}),a.display({id:"type",cell:()=>(0,r.jsx)(u.G3,{value:"Field"}),header:"Type"}),a.display({id:"classifications",cell:e=>{let{row:t}=e;return(0,r.jsx)(L,{resource:t.original})},meta:{overflow:"visible",disableRowClick:!0},header:"Data category",minSize:280}),a.accessor(e=>e.updated_at,{id:"time",cell:e=>(0,r.jsx)(C.Cy,{time:e.getValue()}),header:e=>(0,r.jsx)(u.Rr,{value:"When",...e})}),a.display({id:"actions",cell:e=>(0,r.jsx)(b.Z,{resource:e.row.original}),header:"Actions"})]}:{columns:[]}};(i=s||(s={}))[i.ACTION_REQUIRED=0]="ACTION_REQUIRED",i[i.UNMONITORED=1]="UNMONITORED";var N=e=>{let{initialFilterTabIndex:t=0}=e,[a,i]=(0,d.useState)(t),s=(0,d.useMemo)(()=>[{label:"Action Required",filters:[v.LL.CLASSIFICATION_ADDITION,v.LL.CLASSIFICATION_UPDATE],childFilters:[v.LL.CLASSIFICATION_ADDITION,v.LL.CLASSIFICATION_UPDATE]},{label:"In progress",filters:[v.LL.CLASSIFYING,v.LL.CLASSIFICATION_QUEUED],childFilters:[v.LL.CLASSIFYING,v.LL.CLASSIFICATION_QUEUED]},{label:"Unmonitored",filters:[v.LL.MUTED],childFilters:[]}],[]);return{filterTabs:s,filterTabIndex:a,setFilterTabIndex:i,activeDiffFilters:s[a].filters,activeChildDiffFilters:s[a].childFilters}},V=a(38637),D=a(87573),A=a(35682),M=e=>{let{resourceUrn:t}=e,[a,{isLoading:i}]=(0,g.Hf)(),[s,{isLoading:n}]=(0,g.zV)(),l=i||n,c=async e=>{await s({staged_resource_urns:e})},d=async e=>{await a({staged_resource_urns:e})};return(0,r.jsx)(o.kCb,{direction:"row",align:"center",justify:"center","data-testid":"bulk-actions-menu",children:(0,r.jsxs)("div",{className:"flex gap-2",children:[(0,r.jsx)(A.Z,{title:"Confirm all",icon:(0,r.jsx)(o.nQG,{}),onClick:()=>d([t]),disabled:l,loading:i,type:"primary"}),(0,r.jsx)(A.Z,{title:"Ignore all",icon:(0,r.jsx)(o.tpL,{}),onClick:()=>c([t]),disabled:l,loading:n})]})})},R=e=>{let{selectedUrns:t}=e,[a,{isLoading:i}]=(0,g.Hf)(),[s,{isLoading:n}]=(0,g.zV)(),l=i||n,c=async e=>{await a({staged_resource_urns:e})},d=async e=>{await s({staged_resource_urns:e})};return t.length?(0,r.jsxs)(o.kCb,{direction:"row",align:"center",justify:"center","data-testid":"bulk-actions-menu",children:[(0,r.jsx)(o.xvT,{fontSize:"xs",fontWeight:"semibold",minW:16,mr:6,children:"".concat(t.length," selected")}),(0,r.jsxs)("div",{children:[(0,r.jsx)(A.Z,{title:"Confirm",icon:(0,r.jsx)(o.nQG,{}),onClick:()=>c(t),disabled:l,loading:i,type:"primary"}),(0,r.jsx)(A.Z,{title:"Ignore",icon:(0,r.jsx)(o.tpL,{}),disabled:l,loading:n,onClick:()=>d(t)})]})]}):null},H=a(52962),k=a(71329),z=a(2053),F=a(22770);let E={items:[],total:0,page:1,size:50,pages:1},O=()=>(0,r.jsx)(o.gCW,{mt:6,p:10,spacing:4,borderRadius:"base",maxW:"70%","data-testid":"empty-state",alignSelf:"center",margin:"auto",children:(0,r.jsxs)(o.gCW,{children:[(0,r.jsx)(o.xvT,{fontSize:"md",fontWeight:"600",children:"No activity found"}),(0,r.jsx)(o.xvT,{fontSize:"sm",children:"You're up to date!"})]})});var U=e=>{var t,a;let{resourceUrn:i}=e,C=(0,c.useRouter)(),[m,h]=(0,d.useState)(""),{filterTabs:f,setFilterTabIndex:j,filterTabIndex:v,activeDiffFilters:b,activeChildDiffFilters:y}=N({initialFilterTabIndex:(null===(t=C.query)||void 0===t?void 0:t.filterTabIndex)?Number(null===(a=C.query)||void 0===a?void 0:a.filterTabIndex):void 0}),[I,_]=(0,d.useState)({}),{PAGE_SIZES:S,pageSize:w,setPageSize:L,onPreviousPageClick:Z,isPreviousPageDisabled:A,onNextPageClick:U,isNextPageDisabled:P,startRange:W,endRange:G,pageIndex:Q,setTotalPages:B,resetPageIndexToDefault:q}=(0,u.oi)();(0,d.useEffect)(()=>{q()},[i,m,q,b,y]);let{isFetching:X,isLoading:Y,data:$}=(0,g.z8)({staged_resource_urn:i,page:Q,size:w,child_diff_status:y,diff_status:b,search:m}),K=(0,H.G)(null==$?void 0:$.items[0]),{items:J,total:ee,pages:et}=(0,d.useMemo)(()=>null!=$?$:E,[$]);(0,d.useEffect)(()=>{B(et)},[et,B]);let{columns:ea}=T({resourceType:K}),ei=(0,d.useMemo)(()=>ea,[ea]),{navigateToDiscoveryResults:es}=(0,V.Z)(),er=(0,n.b7)({getCoreRowModel:(0,l.sC)(),getGroupedRowModel:(0,l.qe)(),getExpandedRowModel:(0,l.rV)(),columns:ei,manualPagination:!0,onRowSelectionChange:_,state:{rowSelection:I},getRowId:k.Z,data:J,columnResizeMode:"onChange"}),en=Object.keys(I).filter(e=>I[e]);return Y?(0,r.jsx)(u.I4,{rowHeight:36,numRows:36}):(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(x.Z,{filterTabs:f,filterTabIndex:v,onChange:j}),(0,r.jsxs)(u.Q$,{children:[(0,r.jsxs)(o.kCb,{gap:6,align:"center",children:[(0,r.jsx)(o.xuv,{flexShrink:0,children:(0,r.jsx)(F.M,{value:m,onChange:h})}),(0,r.jsx)(D.Z,{})]}),K===p.X.TABLE&&!!en.length&&(0,r.jsx)(R,{selectedUrns:en}),K===p.X.FIELD&&v!==s.UNMONITORED&&(0,r.jsx)(M,{resourceUrn:i})]}),(0,r.jsx)(u.ZK,{tableInstance:er,onRowClick:e=>es({resourceUrn:e.urn,filterTabIndex:v}),getRowIsClickable:e=>K!==p.X.FIELD||(0,z.Z)(e),emptyTableNotice:(0,r.jsx)(O,{})}),(0,r.jsx)(u.s8,{totalRows:ee||0,pageSizes:S,setPageSize:L,onPreviousPageClick:Z,isPreviousPageDisabled:A||X,onNextPageClick:U,isNextPageDisabled:P||X,startRange:W,endRange:G})]})}},33890:function(e,t,a){"use strict";var i=a(24246),s=a(5152),r=a(53359),n=a(10284),l=a(35682),o=a(6111);t.Z=e=>{let{resource:t}=e,[a,{isLoading:c}]=(0,o.cM)(),[d,{isLoading:u}]=(0,o.vi)(),x=c||u,{diff_status:g,child_diff_statuses:C,top_level_field_name:m}=t,{successAlert:h}=(0,r.V)(),f=g===n.LL.CLASSIFICATION_ADDITION||g===n.LL.CLASSIFICATION_UPDATE,p=C&&(C[n.LL.CLASSIFICATION_ADDITION]||C[n.LL.CLASSIFICATION_UPDATE]),j=(f||p)&&!m,v=f||p;return(0,i.jsxs)(s.Ugi,{onClick:e=>e.stopPropagation(),children:[j&&(0,i.jsx)(l.Z,{title:"Confirm",icon:(0,i.jsx)(s.nQG,{}),onClick:async()=>{await a({staged_resource_urn:t.urn}),h('These changes have been added to a Fides dataset. To view, navigate to "Manage datasets".',"Table changes confirmed")},disabled:x,loading:c}),v&&(0,i.jsx)(l.Z,{title:"Ignore",icon:(0,i.jsx)(s.tpL,{}),onClick:async()=>{await d({staged_resource_urn:t.urn}),h("Ignored changes will not be added to a Fides dataset.","".concat(t.name||"Changes"," ignored"))},disabled:x,loading:u})]})}},61934:function(e,t,a){"use strict";var i=a(24246),s=a(5152);t.Z=e=>{let{type:t}=e;return(0,i.jsx)(s.kCb,{align:"center",h:"full",children:!!t&&(0,i.jsx)(s.Cts,{fontSize:"xs",fontWeight:"normal",children:t})})}},55372:function(e){e.exports={option:"TaxonomySelect_option__vY6v2"}}}]);