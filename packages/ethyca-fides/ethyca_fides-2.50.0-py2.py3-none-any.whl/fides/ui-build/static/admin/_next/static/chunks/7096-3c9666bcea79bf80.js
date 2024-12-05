"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7096],{81836:function(e,t,n){var i=n(24246),l=n(27378),r=n(5152),a=n(79894),s=n.n(a);t.Z=e=>{let{breadcrumbs:t,fontSize:n="2xl",fontWeight:a="semibold",separator:o="->",lastItemStyles:c={color:"black"},normalItemStyles:d={color:"gray.500"},...u}=e;return(0,i.jsx)(r.aGc,{separator:o,fontSize:n,fontWeight:a,"data-testid":"breadcrumbs",...u,children:t.map((e,n)=>{let a=n+1===t.length;return e.title?(0,l.createElement)(r.gN6,{...d,...a?c:{},key:e.title,children:[(null==e?void 0:e.icon)&&(0,i.jsx)(r.xuv,{mr:2,children:e.icon}),e.link?(0,i.jsx)(r.Atw,{as:s(),href:e.link,isCurrentPage:a,children:e.title}):(0,i.jsx)(r.Atw,{_hover:{textDecoration:"none",cursor:"default"},isCurrentPage:a,children:e.title})]}):null})})}},72809:function(e,t,n){var i=n(24246),l=n(5152),r=n(27378);let a=e=>{let t=e.split("."),n=[];return t.forEach(e=>{let t=n.length>0?n[n.length-1]:null;t?n.push("".concat(t,".").concat(e)):n.push(e)}),n},s=(e,t)=>{let n=a(t).filter(e=>e!==t);return e.filter(e=>n.includes(e)).length>0},o=(e,t)=>!!(e===t||e.startsWith("".concat(t,"."))),c=(e,t,n)=>{let i=null!=n?n:[];return e.forEach(e=>{e.children&&c(e.children,t,i),o(e.value,t)&&i.push(e)}),i},d=e=>{let{node:t,isChecked:n,onChecked:r,isExpanded:a,onExpanded:s,isIndeterminate:o,isDisabled:c,children:d}=e,{value:u,label:x}=t,h=!!t.children&&t.children.length>0;return(0,i.jsxs)(l.xuv,{children:[(0,i.jsxs)(l.xuv,{display:"flex",justifyContent:"space-between",_hover:{backgroundColor:"gray.100",cursor:"pointer"},onClick:()=>s(t),minHeight:8,children:[(0,i.jsx)(l.XZJ,{colorScheme:"complimentary",value:u,isChecked:!o&&n,isIndeterminate:o,isDisabled:c,onChange:()=>r(t),mx:2,"data-testid":"checkbox-".concat(x),children:x}),h?(0,i.jsx)(l.wpx,{"data-testid":"expand-".concat(x),"aria-label":a?"collapse":"expand",icon:(0,i.jsx)(l.v4q,{boxSize:5}),type:"text",onClick:()=>s(t),className:a?"rotate-180":void 0}):null]}),d&&(0,i.jsx)(l.xuv,{ml:5,children:d})]})};t.ZP=e=>{let{nodes:t,selected:n,onSelected:u,...x}=e,[h,f]=(0,r.useState)([]),[p,C]=(0,r.useState)([]);(0,r.useEffect)(()=>{let e=Array.from(new Set([...n.map(e=>a(e)).reduce((e,t)=>e.concat(t),[]),...n.map(e=>c(t,e)).reduce((e,t)=>e.concat(t),[]).map(e=>e.value)]));C(e),f(e)},[n,t]);let m=e=>{let i=[],l=[];h.indexOf(e.value)>=0?(i=h.filter(t=>!o(t,e.value)),l=n.filter(t=>!o(t,e.value))):(i=[...h,...c(t,e.value).map(e=>e.value)],l=[...n,e.value]),f(i),u(l)},v=e=>{p.indexOf(e.value)>=0?C(p.filter(t=>!o(t,e.value))):C([...p,e.value])},j=e=>{if(e.children){let l=h.indexOf(e.value)>=0,a=p.indexOf(e.value)>=0,o=c(t,e.value),u=l&&e.children.length>0&&h.filter(t=>t.startsWith("".concat(e.value,"."))).length+1!==o.length,x=s(n,e.value);return(0,i.jsx)(d,{node:e,isChecked:l,onChecked:m,isExpanded:a,onExpanded:v,isDisabled:x,isIndeterminate:u,children:a?e.children.map(e=>(0,i.jsx)(r.Fragment,{children:j(e)},e.value)):void 0})}return null};return(0,i.jsx)(l.xuv,{...x,children:t.map(e=>(0,i.jsx)(l.xuv,{children:j(e)},e.value))})}},57311:function(e,t,n){n.d(t,{Gn:function(){return s},zR:function(){return a}});var i=n(24246),l=n(5152),r=n(79711);let a=e=>{let{title:t}=e;return(0,i.jsx)(l.OXI,{py:0,display:"flex",alignItems:"flex-start",children:(0,i.jsx)(l.xvT,{mr:"2",color:"gray.700",fontSize:"lg",lineHeight:1.8,children:t})})},s=e=>{let{onDelete:t,onEditYaml:n,formId:a,isSaving:s}=e;return(0,i.jsxs)(l.zeN,{justifyContent:"space-between",children:[t?(0,i.jsx)(l.wpx,{"aria-label":"delete",icon:(0,i.jsx)(r.q,{fontSize:"small"}),onClick:t,"data-testid":"delete-btn"}):null,(0,i.jsxs)("div",{className:"flex gap-2",children:[n&&(0,i.jsx)(l.wpx,{onClick:n,"data-testid":"edit-yaml-btn",children:"Edit YAML"}),(0,i.jsx)(l.wpx,{htmlType:"submit",type:"primary","data-testid":"save-btn",form:a,loading:s,children:"Save"})]})]})};t.ZP=e=>{let{header:t,description:n,isOpen:r,onClose:a,children:s,footer:o}=e;return(0,i.jsxs)(l.dys,{placement:"right",isOpen:r,onClose:a,size:"md",children:[(0,i.jsx)(l.P1B,{}),(0,i.jsxs)(l.scA,{"data-testid":"edit-drawer-content",py:2,children:[(0,i.jsxs)(l.xuv,{display:"flex",justifyContent:"space-between",alignItems:"top",mr:2,py:2,gap:2,children:[(0,i.jsx)(l.xuv,{flex:1,minH:8,children:t}),(0,i.jsx)(l.xuv,{display:"flex",justifyContent:"flex-end",mr:2,children:(0,i.jsx)(l.wpx,{"aria-label":"Close editor",onClick:a,"data-testid":"close-drawer-btn",icon:(0,i.jsx)(l.Two,{fontSize:"smaller"})})})]}),(0,i.jsxs)(l.Ng0,{pt:1,children:[n?(0,i.jsx)(l.xvT,{fontSize:"sm",mb:4,color:"gray.600",children:n}):null,s]}),o]})]})}},79711:function(e,t,n){n.d(t,{q:function(){return l}});var i=n(24246);let l=(0,n(5152).IUT)({displayName:"TrashCanOutlineIcon",viewBox:"0 0 11 12",path:(0,i.jsx)("path",{d:"M4.5166 1.60859L4.1084 2.21875H7.22363L6.81543 1.60859C6.7832 1.56133 6.72949 1.53125 6.67148 1.53125H4.6584C4.60039 1.53125 4.54668 1.55918 4.51445 1.60859H4.5166ZM7.6748 1.03711L8.46328 2.21875H8.75977H9.79102H9.96289C10.2486 2.21875 10.4785 2.44863 10.4785 2.73438C10.4785 3.02012 10.2486 3.25 9.96289 3.25H9.79102V9.78125C9.79102 10.7309 9.02188 11.5 8.07227 11.5H3.25977C2.31016 11.5 1.54102 10.7309 1.54102 9.78125V3.25H1.36914C1.0834 3.25 0.853516 3.02012 0.853516 2.73438C0.853516 2.44863 1.0834 2.21875 1.36914 2.21875H1.54102H2.57227H2.86875L3.65723 1.03496C3.88066 0.701953 4.25664 0.5 4.6584 0.5H6.67148C7.07324 0.5 7.44922 0.701953 7.67266 1.03496L7.6748 1.03711ZM2.57227 3.25V9.78125C2.57227 10.1615 2.87949 10.4688 3.25977 10.4688H8.07227C8.45254 10.4688 8.75977 10.1615 8.75977 9.78125V3.25H2.57227ZM4.29102 4.625V9.09375C4.29102 9.28281 4.13633 9.4375 3.94727 9.4375C3.7582 9.4375 3.60352 9.28281 3.60352 9.09375V4.625C3.60352 4.43594 3.7582 4.28125 3.94727 4.28125C4.13633 4.28125 4.29102 4.43594 4.29102 4.625ZM6.00977 4.625V9.09375C6.00977 9.28281 5.85508 9.4375 5.66602 9.4375C5.47695 9.4375 5.32227 9.28281 5.32227 9.09375V4.625C5.32227 4.43594 5.47695 4.28125 5.66602 4.28125C5.85508 4.28125 6.00977 4.43594 6.00977 4.625ZM7.72852 4.625V9.09375C7.72852 9.28281 7.57383 9.4375 7.38477 9.4375C7.1957 9.4375 7.04102 9.28281 7.04102 9.09375V4.625C7.04102 4.43594 7.1957 4.28125 7.38477 4.28125C7.57383 4.28125 7.72852 4.43594 7.72852 4.625Z",fill:"currentColor"})})},90824:function(e,t,n){n.d(t,{V:function(){return l}});var i=n(24246);let l=(0,n(5152).IUT)({displayName:"DatabaseIcon",viewBox:"0 0 12 12",path:(0,i.jsx)("path",{fill:"currentColor",d:"M6 12C4.32222 12 2.90278 11.7417 1.74167 11.225C0.580556 10.7083 0 10.0778 0 9.33333V2.66667C0 1.93333 0.586111 1.30556 1.75833 0.783333C2.93056 0.261111 4.34444 0 6 0C7.65556 0 9.06944 0.261111 10.2417 0.783333C11.4139 1.30556 12 1.93333 12 2.66667V9.33333C12 10.0778 11.4194 10.7083 10.2583 11.225C9.09722 11.7417 7.67778 12 6 12ZM6 4.01667C6.98889 4.01667 7.98333 3.875 8.98333 3.59167C9.98333 3.30833 10.5444 3.00556 10.6667 2.68333C10.5444 2.36111 9.98611 2.05556 8.99167 1.76667C7.99722 1.47778 7 1.33333 6 1.33333C4.98889 1.33333 3.99722 1.475 3.025 1.75833C2.05278 2.04167 1.48889 2.35 1.33333 2.68333C1.48889 3.01667 2.05278 3.32222 3.025 3.6C3.99722 3.87778 4.98889 4.01667 6 4.01667ZM6 7.33333C6.46667 7.33333 6.91667 7.31111 7.35 7.26667C7.78333 7.22222 8.19722 7.15833 8.59167 7.075C8.98611 6.99167 9.35833 6.88889 9.70833 6.76667C10.0583 6.64444 10.3778 6.50556 10.6667 6.35V4.35C10.3778 4.50556 10.0583 4.64444 9.70833 4.76667C9.35833 4.88889 8.98611 4.99167 8.59167 5.075C8.19722 5.15833 7.78333 5.22222 7.35 5.26667C6.91667 5.31111 6.46667 5.33333 6 5.33333C5.53333 5.33333 5.07778 5.31111 4.63333 5.26667C4.18889 5.22222 3.76944 5.15833 3.375 5.075C2.98056 4.99167 2.61111 4.88889 2.26667 4.76667C1.92222 4.64444 1.61111 4.50556 1.33333 4.35V6.35C1.61111 6.50556 1.92222 6.64444 2.26667 6.76667C2.61111 6.88889 2.98056 6.99167 3.375 7.075C3.76944 7.15833 4.18889 7.22222 4.63333 7.26667C5.07778 7.31111 5.53333 7.33333 6 7.33333ZM6 10.6667C6.51111 10.6667 7.03056 10.6278 7.55833 10.55C8.08611 10.4722 8.57222 10.3694 9.01667 10.2417C9.46111 10.1139 9.83333 9.96945 10.1333 9.80833C10.4333 9.64722 10.6111 9.48333 10.6667 9.31667V7.68333C10.3778 7.83889 10.0583 7.97778 9.70833 8.1C9.35833 8.22222 8.98611 8.325 8.59167 8.40833C8.19722 8.49167 7.78333 8.55556 7.35 8.6C6.91667 8.64444 6.46667 8.66667 6 8.66667C5.53333 8.66667 5.07778 8.64444 4.63333 8.6C4.18889 8.55556 3.76944 8.49167 3.375 8.40833C2.98056 8.325 2.61111 8.22222 2.26667 8.1C1.92222 7.97778 1.61111 7.83889 1.33333 7.68333V9.33333C1.38889 9.5 1.56389 9.66111 1.85833 9.81667C2.15278 9.97222 2.52222 10.1139 2.96667 10.2417C3.41111 10.3694 3.9 10.4722 4.43333 10.55C4.96667 10.6278 5.48889 10.6667 6 10.6667Z"})})},62257:function(e,t,n){n.d(t,{l:function(){return l}});var i=n(24246);let l=(0,n(5152).IUT)({displayName:"DatasetIcon",viewBox:"0 0 16 16",path:(0,i.jsx)("path",{fill:"currentColor",d:"M2 14V2H14V14H2ZM3.33333 12.6667H12.6667V3.33333H3.33333V12.6667ZM4.66667 7.33333H7.33333V4.66667H4.66667V7.33333ZM8.66667 7.33333H11.3333V4.66667H8.66667V7.33333ZM4.66667 11.3333H7.33333V8.66667H4.66667V11.3333ZM8.66667 11.3333H11.3333V8.66667H8.66667V11.3333Z"})})},43124:function(e,t,n){n.d(t,{Z:function(){return x}});var i=n(24246),l=n(5152),r=n(88038),a=n.n(r),s=n(86677);n(27378);var o=n(11596),c=n(72247),d=n(11032),u=()=>{let e=(0,s.useRouter)();return(0,i.jsx)(l.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,i.jsxs)(l.xuv,{children:[(0,i.jsxs)(l.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,i.jsx)(l.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,i.jsx)(l.wpx,{onClick:()=>{e.push(d.fz)},children:"Configure"})]}),(0,i.jsxs)(l.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},x=e=>{let{children:t,title:n,padded:r=!0,mainProps:d}=e,x=(0,o.hz)(),h=(0,s.useRouter)(),f="/privacy-requests"===h.pathname||"/datastore-connection"===h.pathname,p=!(x.flags.privacyRequestsConfiguration&&f),{data:C}=(0,c.JE)(void 0,{skip:p}),{data:m}=(0,c.PW)(void 0,{skip:p}),v=x.flags.privacyRequestsConfiguration&&(!C||!m)&&f;return(0,i.jsxs)(l.kCb,{"data-testid":n,direction:"column",h:"100vh",children:[(0,i.jsxs)(a(),{children:[(0,i.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,i.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,i.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,i.jsxs)(l.kCb,{as:"main",direction:"column",py:r?6:0,px:r?10:0,h:r?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...d,children:[v?(0,i.jsx)(u,{}):null,t]})]})}},37541:function(e,t,n){var i=n(24246),l=n(5152),r=n(19785),a=n.n(r),s=n(27378),o=n(81836);t.Z=e=>{let{breadcrumbs:t,isSticky:n=!0,children:r,rightContent:c,...d}=e;return(0,i.jsxs)(l.xuv,{bgColor:"white",paddingY:5,...n?{position:"sticky",top:0,left:0,zIndex:10}:{},...d,children:[(0,i.jsxs)(l.kCb,{alignItems:"flex-start",children:[(0,i.jsxs)(l.xuv,{flex:1,children:[a()(t)&&(0,i.jsx)(l.xuv,{marginBottom:r?4:0,children:(0,i.jsx)(o.Z,{breadcrumbs:t})}),(0,s.isValidElement)(t)&&t]}),c&&(0,i.jsx)(l.xuv,{children:c})]}),r]})}},39006:function(e,t,n){var i=n(24246);n(27378);var l=n(81836);t.Z=e=>(0,i.jsx)(l.Z,{...e,fontSize:"sm",fontWeight:"normal",mt:-1,mb:0,whiteSpace:"nowrap",overflow:"auto",separator:"/",lastItemStyles:{color:"black",fontWeight:"semibold"}})},98894:function(e,t,n){n.d(t,{e:function(){return j},Z:function(){return g}});var i=n(24246),l=n(5152),r=n(34090),a=n(27378),s=n(45007),o=n(9043);let c=e=>{let{dataCategories:t,mostLikelyCategories:n}=e;return(null==t?void 0:t.length)?t:(null==n?void 0:n.length)?[n.reduce((e,t)=>{var n,i;return(null!==(n=t.confidence)&&void 0!==n?n:0)>(null!==(i=e.confidence)&&void 0!==i?i:0)?t:e}).fides_key]:[]};var d=n(96878),u=n(35249),x=n(64712),h=n(39514),f=n(92953),p=n(72809),C=n(62091),m=e=>{let{dataCategories:t,checked:n,onChecked:r,buttonLabel:s}=e,o=(0,a.useMemo)(()=>(0,C.C)(t),[t]);return(0,i.jsxs)(l.v2r,{closeOnSelect:!0,children:[(0,i.jsx)(l.j2t,{as:l.wpx,icon:(0,i.jsx)(l.mCO,{}),className:"!bg-transparent",block:!0,"data-testid":"data-category-dropdown",children:null!=s?s:"Select data categories"}),(0,i.jsx)(l.qyq,{children:(0,i.jsxs)(l.xuv,{maxHeight:"50vh",minWidth:"300px",maxW:"full",overflowY:"scroll",children:[(0,i.jsxs)(l.xuv,{position:"sticky",top:0,zIndex:1,backgroundColor:"white",pt:1,children:[(0,i.jsx)(l.__7,{children:(0,i.jsxs)(l.xuv,{display:"flex",justifyContent:"space-between",px:2,mb:2,children:[(0,i.jsx)(l.sNh,{as:l.wpx,size:"small",className:"mr-2 !w-auto",onClick:()=>r([]),closeOnSelect:!1,"data-testid":"data-category-clear-btn",children:"Clear"}),(0,i.jsx)(l.xvT,{mr:2,children:"Data Categories"}),(0,i.jsx)(l.sNh,{as:l.wpx,size:"small",className:"!w-auto","data-testid":"data-category-done-btn",children:"Done"})]})}),(0,i.jsx)(l.RaW,{})]}),(0,i.jsx)(l.xuv,{px:2,"data-testid":"data-category-checkbox-tree",children:(0,i.jsx)(p.ZP,{nodes:o,selected:n,onSelected:r})})]})})]})},v=e=>{let{dataCategories:t,mostLikelyCategories:n,checked:r,onChecked:a,tooltip:s}=e,o=e=>{a(r.filter(t=>t!==e))},c=r.slice().sort((e,t)=>e.localeCompare(t));return(0,i.jsxs)(l.rjZ,{templateColumns:"1fr 3fr",children:[(0,i.jsx)(l.lXp,{children:"Data Categories"}),n?(0,i.jsxs)(l.xuv,{display:"flex",alignItems:"center",children:[(0,i.jsx)(l.xuv,{mr:"2",width:"100%",children:(0,i.jsx)(l.P$4,{dataCategories:t,mostLikelyCategories:n,checked:r,onChecked:a})}),(0,i.jsx)(h.Z,{label:s})]}):(0,i.jsxs)(l.Kqy,{children:[(0,i.jsxs)(l.xuv,{display:"flex",alignItems:"center",children:[(0,i.jsx)(l.xuv,{mr:"2",width:"100%",children:(0,i.jsx)(m,{dataCategories:t,checked:r,onChecked:a})}),(0,i.jsx)(h.Z,{label:s})]}),(0,i.jsx)(l.Kqy,{"data-testid":"selected-categories",children:c.map(e=>(0,i.jsx)(f.Z,{name:e,onClose:()=>{o(e)}},e))})]})]})};let j="edit-collection-or-field-form";var g=e=>{var t;let{values:n,onSubmit:h,dataType:f,showDataCategories:p=!0}=e,C={description:null!==(t=n.description)&&void 0!==t?t:"",data_categories:n.data_categories},m=(0,s.v9)(u.qb).filter(e=>e.active),g=(0,s.v9)(d.t6),y=(0,a.useMemo)(()=>{var e,t;if(!(m&&g))return;let n=new Map(m.map(e=>[e.fides_key,e]));return null!==(t=null===(e=g.classifications)||void 0===e?void 0:e.map(e=>{let{label:t,score:i}=e,l=n.get(t);return{fides_key:t,confidence:i,...l}}))&&void 0!==t?t:[]},[m,g]),[b,k]=(0,a.useState)(()=>c({dataCategories:C.data_categories,mostLikelyCategories:y})),w="collection"===f?x.du.description.tooltip:x.QL.description.tooltip,V="collection"===f?x.du.data_categories.tooltip:x.QL.data_categories.tooltip;return(0,i.jsx)(r.J9,{initialValues:C,onSubmit:e=>{h({...e,data_categories:b})},children:(0,i.jsx)(r.l0,{id:j,children:(0,i.jsxs)(l.Kqy,{children:[(0,i.jsx)(o.j0,{name:"description",label:"Description",tooltip:w,"data-testid":"description-input"}),p&&(0,i.jsx)(v,{dataCategories:m,mostLikelyCategories:y,checked:b,onChecked:k,tooltip:V})]})})})}},64712:function(e,t,n){n.d(t,{QL:function(){return r},du:function(){return l},tz:function(){return i}});let i={name:{tooltip:"A UI-friendly label for the Dataset."},description:{tooltip:"A human-readable description of the Dataset."},data_categories:{tooltip:"Arrays of Data Category resources, identified by fides_key, that apply to all collections in the Dataset."}},l={description:{tooltip:"A human-readable description of the collection."},data_categories:{tooltip:"Arrays of Data Category resources, identified by fides_key, that apply to all fields in the collection."}},r={description:{tooltip:"A human-readable description of the field."},data_categories:{tooltip:"Arrays of Data Category resources, identified by fides_key, that apply to this field."}}},5067:function(e,t,n){n.d(t,{Fk:function(){return c},_n:function(){return s},jC:function(){return r},qe:function(){return o}});var i=n(99729),l=n.n(i);let r=(e,t,n)=>{let i=e.collections.map((e,i)=>i===n?t:e);return{...e,collections:i}},a=(e,t,n)=>{let i=e.fields.map((e,i)=>i===n?t:e);return{...e,fields:i}},s=(e,t,n,i)=>{let l=a(e.collections[n],t,i);return r(e,l,n)},o=(e,t)=>{let n=e.collections.filter((e,n)=>n!==t);return{...e,collections:n}},c=e=>{let{dataset:t,collectionName:n,subfields:i}=e,r="",a=t.collections.findIndex(e=>e.name===n);return r+="collections[".concat(a,"]"),i&&i.forEach(e=>{let n=l()(t,r).fields.findIndex(t=>t.name===e);r+=".fields[".concat(n,"]")}),r}},92953:function(e,t,n){var i=n(24246),l=n(5152);t.Z=e=>{let{name:t,onClose:n,...r}=e,a={backgroundColor:"primary.400",color:"white","data-testid":"taxonomy-entity-".concat(t),width:"fit-content",size:"sm",...r};return n?(0,i.jsxs)(l.Vp9,{display:"flex",justifyContent:"space-between",...a,children:[(0,i.jsx)(l.Sn0,{children:t}),(0,i.jsx)(l.SD9,{onClick:n,color:"white"})]}):(0,i.jsx)(l.Vp9,{...a,children:t})}},62091:function(e,t,n){n.d(t,{C:function(){return i},P:function(){return l}});let i=(e,t)=>{let n;if(null==t&&e.every(e=>void 0===e.parent_key))n=e;else{let i=null!=t?t:null;n=e.filter(e=>e.parent_key===i)}return n.map(t=>{var n,l;let r=t.fides_key;return{value:t.fides_key,label:""===t.name||null==t.name?t.fides_key:t.name,description:t.description,children:i(e,r),is_default:null!==(n=t.is_default)&&void 0!==n&&n,active:null!==(l=t.active)&&void 0!==l&&l}})},l=e=>{let t=e.split(".");return 1===t.length?"":t.slice(0,t.length-1).join(".")}}}]);