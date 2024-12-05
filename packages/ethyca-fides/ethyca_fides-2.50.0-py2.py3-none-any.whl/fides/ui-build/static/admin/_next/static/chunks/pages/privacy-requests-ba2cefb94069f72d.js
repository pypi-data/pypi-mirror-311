(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2369],{1565:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/privacy-requests",function(){return r(32474)}])},65464:function(e,t,r){"use strict";var l=r(24246),i=r(5152),n=r(88038),s=r.n(n);r(27378),t.Z=e=>{let{children:t,title:r,mainProps:n}=e;return(0,l.jsxs)(i.kCb,{"data-testid":r,direction:"column",height:"calc(100vh - 48px)",width:"calc(100vw - 200px)",children:[(0,l.jsxs)(s(),{children:[(0,l.jsxs)("title",{children:["Fides Admin UI - ",r]}),(0,l.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,l.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,l.jsx)(i.kCb,{pt:6,as:"main",overflow:"auto",direction:"column",flex:1,minWidth:0,...n,children:t})]})}},37440:function(e,t,r){"use strict";var l=r(24246),i=r(5152);t.Z=e=>{let{title:t,text:r,onClose:n}=e;return(0,l.jsxs)(i.Ugi,{backgroundColor:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",py:4,pr:6,pl:3,"data-testid":"empty-state",gap:2,position:"relative",children:[n&&(0,l.jsx)(i.Two,{boxSize:5,position:"absolute",right:3,top:3,zIndex:1,cursor:"pointer",p:1,onClick:n}),(0,l.jsx)(i.iid,{alignSelf:"start",color:"blue.400",mt:.5,flexGrow:0}),(0,l.jsxs)(i.kCb,{direction:"column",gap:2,flexGrow:1,children:[(0,l.jsx)(i.X6q,{fontSize:"md",children:t}),(0,l.jsx)(i.xvT,{fontSize:"sm",color:"gray.600",lineHeight:"5",children:r})]})]})}},38615:function(e,t,r){"use strict";r.d(t,{Tg:function(){return s}});var l=r(24246),i=r(44296),n=r(96451);let s=e=>(0,i.C)(n.uu).filter(t=>e.includes(t)).length>0;t.ZP=e=>{let{scopes:t,children:r}=e;return s(t)?(0,l.jsx)(l.Fragment,{children:r}):null}},53359:function(e,t,r){"use strict";r.d(t,{H:function(){return n},V:function(){return l.V}});var l=r(75139),i=r(60136);let n=()=>{let{errorAlert:e}=(0,l.V)();return{handleError:t=>{let r="An unexpected error occurred. Please try again.";(0,i.Ot)(t)?r=t.data.detail:(0,i.tB)(t)&&(r=t.data.detail[0].msg),e(r)}}}},75139:function(e,t,r){"use strict";r.d(t,{V:function(){return n}});var l=r(24246),i=r(5152);let n=()=>{let e=(0,i.pmc)();return{errorAlert:(t,r,n)=>{let s={...n,position:(null==n?void 0:n.position)||"top",render:e=>{let{onClose:n}=e;return(0,l.jsxs)(i.bZj,{alignItems:"normal",status:"error",children:[(0,l.jsx)(i.zMQ,{}),(0,l.jsxs)(i.xuv,{children:[r&&(0,l.jsx)(i.CdC,{children:r}),(0,l.jsx)(i.XaZ,{children:t})]}),(0,l.jsx)(i.PZ7,{onClick:n,position:"relative",right:0,size:"sm",top:-1})]})}};(null==n?void 0:n.id)&&e.isActive(n.id)?e.update(n.id,s):e(s)},successAlert:(t,r,n)=>{let s={...n,position:(null==n?void 0:n.position)||"top",render:e=>{let{onClose:n}=e;return(0,l.jsxs)(i.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,l.jsx)(i.zMQ,{}),(0,l.jsxs)(i.xuv,{children:[r&&(0,l.jsx)(i.CdC,{children:r}),(0,l.jsx)(i.XaZ,{children:t})]}),(0,l.jsx)(i.PZ7,{onClick:n,position:"relative",right:0,size:"sm",top:-1})]})}};(null==n?void 0:n.id)&&e.isActive(n.id)?e.update(n.id,s):e(s)}}}},21613:function(e,t,r){"use strict";var l=r(24246),i=r(5152),n=r(27378);t.Z=e=>{let{isOpen:t,onClose:r,onApproveRequest:s,isLoading:a,subjectRequest:o}=e,{identity:d,identity_verified_at:u,custom_privacy_request_fields:c}=o,p=(0,n.useCallback)(()=>{s().then(()=>{r()})},[s,r]);return(0,l.jsxs)(i.u_l,{isOpen:t,onClose:r,size:"lg",isCentered:!0,children:[(0,l.jsx)(i.ZAr,{}),(0,l.jsxs)(i.hzk,{children:[(0,l.jsx)(i.xBx,{children:"Privacy request approval"}),(0,l.jsxs)(i.fef,{paddingTop:0,paddingBottom:0,children:[(0,l.jsx)(i.xvT,{color:"gray.500",fontSize:"14px",marginBottom:4,children:"Are you sure you want to approve this privacy request?"}),(0,l.jsxs)(i.QI$,{children:[Object.entries(d).filter(e=>{let[,{value:t}]=e;return null!==t}).map(e=>{let[t,{value:r,label:n}]=e;return(0,l.jsx)(i.HCh,{children:(0,l.jsxs)(i.kCb,{alignItems:"flex-start",children:[(0,l.jsxs)(i.xvT,{mr:2,fontSize:"sm",color:"gray.900",fontWeight:"500",children:[n,":"]}),(0,l.jsx)(i.xvT,{color:"gray.600",fontWeight:"500",fontSize:"sm",mr:2,children:r}),"(",u?"Verified":"Unverified",")"]},t)},t)}),c&&Object.entries(c).filter(e=>{let[,t]=e;return t.value}).map(e=>{let[t,r]=e;return(0,l.jsx)(i.HCh,{children:(0,l.jsxs)(i.kCb,{alignItems:"flex-start",children:[(0,l.jsxs)(i.xvT,{mr:2,fontSize:"sm",color:"gray.900",fontWeight:"500",children:[r.label,":"]}),(0,l.jsxs)(i.xvT,{color:"gray.600",fontWeight:"500",fontSize:"sm",mr:2,children:[Array.isArray(r.value)?r.value.join(", "):r.value," "]}),"(Unverified)"]},t)},t)})]})]}),(0,l.jsx)(i.mzw,{children:(0,l.jsxs)(i.MIq,{columns:2,width:"100%",children:[(0,l.jsx)(i.wpx,{onClick:r,className:"mr-3","data-testid":"cancel-btn",children:"Cancel"}),(0,l.jsx)(i.wpx,{type:"primary","data-testid":"continue-btn",onClick:p,loading:a,children:"Confirm"})]})})]})]})}},94723:function(e,t,r){"use strict";var l=r(24246),i=r(9043),n=r(5152),s=r(34090),a=r(27378),o=r(59389);let d={denialReason:""};t.Z=e=>{let{isOpen:t,onClose:r,onDenyRequest:u}=e,c=(0,a.useCallback)((e,t)=>{let{setSubmitting:l}=t;u(e.denialReason).then(()=>{l(!1),r()})},[u,r]);return(0,l.jsxs)(n.u_l,{isOpen:t,onClose:r,isCentered:!0,returnFocusOnClose:!1,children:[(0,l.jsx)(n.ZAr,{}),(0,l.jsx)(n.hzk,{width:"100%",maxWidth:"456px","data-testid":"deny-privacy-request-modal",children:(0,l.jsx)(s.J9,{initialValues:d,validationSchema:o.Ry({denialReason:o.Z_().required().label("Reason for denial")}),onSubmit:c,children:e=>{let{isSubmitting:t,dirty:a,isValid:o}=e;return(0,l.jsxs)(s.l0,{children:[(0,l.jsx)(n.xBx,{children:"Privacy request denial"}),(0,l.jsx)(n.fef,{color:"gray.500",fontSize:"14px",children:"Please enter a reason for denying this privacy request. Please note: this can be seen by the user in their notification email."}),(0,l.jsx)(n.fef,{children:(0,l.jsx)(i.Ks,{name:"denialReason",textAreaProps:{focusBorderColor:"primary.600",resize:"none"}})}),(0,l.jsxs)(n.mzw,{className:"flex w-full gap-4",children:[(0,l.jsx)(n.wpx,{disabled:t,onClick:r,className:"grow",children:"Cancel"}),(0,l.jsx)(n.wpx,{htmlType:"submit",type:"primary",disabled:!a||!o,loading:t,className:"grow","data-testid":"deny-privacy-request-modal-btn",children:"Confirm"})]})]})}})})]})}},95758:function(e,t,r){"use strict";r.d(t,{DE:function(){return a},MP:function(){return i},qX:function(){return s},rE:function(){return n}});var l=r(10284);let i=new Map([[l.q2.APPROVED,"Approved"],[l.q2.CANCELED,"Canceled"],[l.q2.COMPLETE,"Completed"],[l.q2.DENIED,"Denied"],[l.q2.ERROR,"Error"],[l.q2.IN_PROCESSING,"In Progress"],[l.q2.PENDING,"New"],[l.q2.PAUSED,"Paused"],[l.q2.IDENTITY_UNVERIFIED,"Unverified"],[l.q2.REQUIRES_INPUT,"Requires input"]]),n=new Map([[l.Us.ACCESS,"Access"],[l.Us.ERASURE,"Erasure"],[l.Us.CONSENT,"Consent"],[l.Us.UPDATE,"Update"]]),s={mailgun:"mailgun",twilio_email:"twilio_email",twilio_text:"twilio_text"},a={local:"local",s3:"s3"}},25662:function(e,t,r){"use strict";r.d(t,{Z:function(){return i}});var l=r(72247);let i=e=>{let{subjectRequest:t}=e,[r,i]=(0,l.RW)({fixedCacheKey:t.id}),[n,s]=(0,l.F1)({fixedCacheKey:t.id}),[a,o]=(0,l.rC)({fixedCacheKey:t.id}),d=s.isLoading||i.isLoading;return{approveRequest:r,approveRequestResult:i,denyRequest:n,denyRequestResult:s,handleApproveRequest:()=>r(t),handleDenyRequest:e=>n({id:t.id,reason:e}),handleDeleteRequest:()=>a(t),softDeleteRequestResult:o,isLoading:d}}},32474:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return es}});var l,i,n=r(24246),s=r(65464),a=r(5152),o=r(65218),d=r.n(o),u=r(27378),c=r(11596),p=r(38615),h=r(59003),x=r(92222),m=r(86677),f=r(45007),y=r(36223),v=r(62528),j=r(8540),b=r(72247),g=r(94167),_=r(95758),C=r(10284);let q={approved:{colorScheme:"green",label:"Approved"},complete:{label:"Completed"},awaiting_email_send:{label:"Awaiting Email Send"},denied:{label:"Denied"},canceled:{label:"Canceled"},error:{colorScheme:"red",label:"Error"},in_processing:{colorScheme:"yellow",label:"In Progress"},paused:{label:"Paused"},pending:{colorScheme:"blue",label:"New"},identity_unverified:{colorScheme:"red",label:"Unverified"},requires_input:{colorScheme:"orange",label:"Requires Input"}},w=e=>{let{value:t}=e;return(0,n.jsx)(j.A4,{colorScheme:q[t].colorScheme,value:q[t].label,"data-testid":"request-status-badge"})},E=e=>{let t,{daysLeft:r,timeframe:l=45,status:i,includeText:s=!1}=e;if(null==r||i===C.q2.COMPLETE||i===C.q2.CANCELED||i===C.q2.DENIED||i===C.q2.IDENTITY_UNVERIFIED)return null;let a=100*r/l;return a<25?t="red":a>=75?t="green":a>=25&&(t="orange"),(0,n.jsx)(j.A4,{value:s?"".concat(r," days left"):r.toString(),colorScheme:t})},R=e=>Array.from(new Set(e.filter(e=>Object.values(C.Us).includes(e.action_type)).map(e=>e.action_type))),S=e=>{let{value:t}=e,r=R(t).map(e=>_.rE.get(e));return(0,n.jsx)(j.WP,{value:r,cellState:{isExpanded:!0}})};var k=r(77650),P=r(21613),T=r(94723),I=r(25662);let A=e=>{let{subjectRequest:t,...r}=e,l=(0,a.qY0)(),i=(0,a.qY0)(),s=(0,a.qY0)(),{handleApproveRequest:o,handleDenyRequest:d,handleDeleteRequest:u,isLoading:c}=(0,I.Z)({subjectRequest:t});return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(a.Ugi,{...r,children:["pending"!==t.status?null:(0,n.jsx)(a.wpx,{title:"Approve","aria-label":"Approve",icon:(0,n.jsx)(a.nQG,{w:2,h:2}),onClick:l.onOpen,loading:c,disabled:c,"data-testid":"privacy-request-approve-btn",size:"small"}),"pending"!==t.status?null:(0,n.jsx)(a.wpx,{title:"Deny","aria-label":"Deny",icon:(0,n.jsx)(a.Two,{w:2,h:2}),onClick:i.onOpen,loading:c,disabled:c,"data-testid":"privacy-request-deny-btn",size:"small"}),(0,n.jsx)(p.ZP,{scopes:[C.Sh.PRIVACY_REQUEST_DELETE],children:(0,n.jsx)(a.wpx,{title:"Delete","aria-label":"Delete",icon:(0,n.jsx)(a.pJl,{w:2,h:2}),onClick:s.onOpen,loading:c,disabled:c,"data-testid":"privacy-request-delete-btn",size:"small"})})]}),(0,n.jsx)(a.h_i,{children:(0,n.jsx)(P.Z,{isOpen:l.isOpen,isLoading:c,onClose:l.onClose,onApproveRequest:o,subjectRequest:t})}),(0,n.jsx)(a.h_i,{children:(0,n.jsx)(T.Z,{isOpen:i.isOpen,onClose:i.onClose,onDenyRequest:d})}),(0,n.jsx)(k.Z,{isOpen:s.isOpen,onClose:s.onClose,onConfirm:u,message:(0,n.jsx)(a.xvT,{children:"You are about to permanently delete the privacy request. Are you sure you would like to continue?"})})]})};(l=i||(i={})).STATUS="status",l.DAYS_LEFT="due_date",l.SOURCE="source",l.REQUEST_TYPE="request_type",l.SUBJECT_IDENTITY="subject_identity",l.TIME_RECEIVED="created_at",l.CREATED_BY="created_by",l.REVIEWER="reviewer",l.ID="id",l.ACTIONS="actions";let O=(0,x.Cl)(),z=function(){let e=arguments.length>0&&void 0!==arguments[0]&&arguments[0];return[O.accessor(e=>e.status,{id:"status",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(w,{value:t()})},header:e=>(0,n.jsx)(j.Rr,{value:"Status",...e})}),O.accessor(e=>e.days_left,{id:"due_date",cell:e=>{let{row:t,getValue:r}=e;return(0,n.jsx)(E,{daysLeft:r(),timeframe:t.original.policy.execution_timeframe,status:t.original.status})},header:e=>(0,n.jsx)(j.Rr,{value:"Days left",...e})}),...e?[O.accessor(e=>e.source,{id:"source",cell:e=>e.getValue()?(0,n.jsx)(j.A4,{value:e.getValue()}):(0,n.jsx)(j.G3,{value:void 0}),header:e=>(0,n.jsx)(j.Rr,{value:"Source",...e}),enableSorting:!1})]:[],O.accessor(e=>e.policy.rules,{id:"request_type",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(S,{value:t()})},header:e=>(0,n.jsx)(j.Rr,{value:"Request type",...e}),enableSorting:!1}),O.accessor(e=>{var t,r;return(null===(t=e.identity)||void 0===t?void 0:t.email.value)||(null===(r=e.identity)||void 0===r?void 0:r.phone_number.value)||""},{id:"subject_identity",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(j.G3,{value:t()})},header:e=>(0,n.jsx)(j.Rr,{value:"Subject identity",...e}),enableSorting:!1}),O.accessor(e=>e.created_at,{id:"created_at",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(j.G3,{value:(0,g.p6)(t())})},header:e=>(0,n.jsx)(j.Rr,{value:"Time received",...e})}),O.accessor(e=>{var t;return(null===(t=e.reviewer)||void 0===t?void 0:t.username)||""},{id:"reviewer",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(j.G3,{value:t()})},header:e=>(0,n.jsx)(j.Rr,{value:"Reviewed by",...e}),enableSorting:!1}),O.accessor(e=>e.id,{id:"id",cell:e=>{let{getValue:t}=e;return(0,n.jsx)(j.G3,{value:t()})},header:e=>(0,n.jsx)(j.Rr,{value:"Request ID",...e}),enableSorting:!1}),O.display({id:"actions",cell:e=>{let{row:t}=e;return(0,n.jsx)(A,{subjectRequest:t.original})},header:e=>(0,n.jsx)(j.Rr,{value:"Actions",...e}),meta:{disableRowClick:!0}})]};var D=e=>{let{defaultValues:t,items:r,onSelection:l}=e,[i,s]=(0,u.useState)(r),o=()=>{l(i)};return(0,n.jsxs)(a.qyq,{lineHeight:"1rem",pt:"0",children:[(0,n.jsxs)(a.kCb,{borderBottom:"1px",borderColor:"gray.200",cursor:"auto",p:"8px",children:[(0,n.jsx)(a.wpx,{onClick:()=>{s(r),l(new Map)},size:"small",children:"Clear"}),(0,n.jsx)(a.LZC,{}),(0,n.jsx)(a.wpx,{type:"primary",onClick:o,size:"small",children:"Done"})]}),(0,n.jsx)(a.xuv,{maxH:"360px",overflow:"auto",children:(0,n.jsx)(a.cOn,{colorScheme:"purple",defaultValue:t,onChange:e=>{let t=new Map(i);t.forEach((e,r)=>{t.set(r,!1)}),e.forEach(e=>{t.set(e,!0)}),s(t)},children:[...r].sort().map(e=>{let[t]=e;return(0,n.jsx)(a.sNh,{p:0,onKeyPress:e=>{" "===e.key&&e.currentTarget.getElementsByTagName("input")[0].click(),"Enter"===e.key&&o()},children:(0,n.jsx)(a.XZJ,{isChecked:r.get(t),spacing:2,value:t,width:"100%",fontSize:"0.75rem",paddingTop:"10px",paddingRight:"8.5px",paddingBottom:"10px",paddingLeft:"8.5px",onClick:e=>e.stopPropagation(),children:t})},t)})})})]})};let Z=e=>{let{closeOnSelect:t=!1,options:r,value:l,onChange:i,placeholder:s="Select one or more items",...o}=e,[d,c]=(0,u.useState)(!1),p=(0,u.useMemo)(()=>(0,g.gv)(r,l),[r,l]),h=(0,u.useMemo)(()=>null==l?void 0:l.map(e=>r.get(e)),[r,l]),x=()=>{c(!1)},m=e=>{let t=(0,g.W)(e,[!0]);i((0,g.W)(r,t)),x()},f=e=>{i(l.filter(t=>t!==e))};return(0,n.jsx)(a.v2r,{isLazy:!0,closeOnSelect:t,onClose:x,onOpen:()=>{c(!0)},children:e=>{let{onClose:t}=e;return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(a.xuv,{sx:{border:"1px solid",borderColor:"gray.200",borderRadius:"md",display:"flex",flexWrap:"wrap",gap:2,py:2,pl:2,pr:10,position:"relative",zIndex:0,...o.sx},children:[(null==l?void 0:l.length)?l.map(e=>(0,n.jsxs)(a.Vp9,{size:"md",zIndex:1,children:[(0,n.jsx)(a.Sn0,{children:r.get(e)}),(0,n.jsx)(a.SD9,{onClick:()=>f(e)})]},e)):s,(0,n.jsx)(a.j2t,{as:a.wpx,icon:(0,n.jsx)(a.mCO,{}),className:"absolute right-0 top-0 border-none !bg-transparent"})]}),d&&(0,n.jsx)(D,{defaultValues:h,items:p,onSelection:e=>{m(e),t()}})]})}})},N=e=>{let t=(0,f.v9)(b.dp),r=(0,f.I0)();return{handleStatusChange:t=>{r((0,b.CI)(t)),e()},handleActionTypeChange:t=>{r((0,b.aM)(t)),e()},handleFromChange:t=>{r((0,b.su)(null==t?void 0:t.target.value)),e()},handleToChange:t=>{r((0,b.Ue)(null==t?void 0:t.target.value)),e()},handleClearAllFilters:()=>{r((0,b.Mk)()),e()},...t}},U=e=>{let{onClose:t,onFilterChange:r,...l}=e,{handleStatusChange:i,handleActionTypeChange:s,handleFromChange:o,handleToChange:d,handleClearAllFilters:u,from:c,to:p,status:h,action_type:x}=N(r);return(0,n.jsxs)(a.u_l,{onClose:t,size:"xl",...l,children:[(0,n.jsx)(a.ZAr,{}),(0,n.jsxs)(a.hzk,{children:[(0,n.jsx)(a.xBx,{borderBottomWidth:1,borderBottomColor:"gray.200",children:"All Filters"}),(0,n.jsx)(a.olH,{}),(0,n.jsx)(a.fef,{py:4,sx:{"& label":{mb:0}},children:(0,n.jsxs)(a.Kqy,{gap:4,children:[(0,n.jsxs)(a.Kqy,{children:[(0,n.jsx)(a.lXp,{size:"md",id:"request-date-range-label",children:"Date range"}),(0,n.jsxs)(a.Ugi,{gap:3,children:[(0,n.jsxs)(a.BZy,{size:"sm",flex:1,children:[(0,n.jsx)(a.UiE,{as:"label",htmlFor:"from-date",borderRadius:"md",children:"From"}),(0,n.jsx)(a.IIB,{type:"date",name:"From",value:c,max:p||void 0,onChange:o,borderRadius:"md",id:"from-date","aria-describedby":"request-date-range-label"})]}),(0,n.jsxs)(a.BZy,{size:"sm",flex:1,children:[(0,n.jsx)(a.UiE,{as:"label",htmlFor:"to-date",borderRadius:"md",children:"To"}),(0,n.jsx)(a.IIB,{type:"date",borderRadius:"md",name:"To",value:p,min:c||void 0,onChange:d,id:"to-date","aria-describedby":"request-date-range-label"})]})]})]}),(0,n.jsxs)(a.Kqy,{children:[(0,n.jsx)(a.lXp,{size:"md",id:"request-status-label",children:"Status"}),(0,n.jsx)(Z,{options:_.MP,value:h,onChange:i,"aria-describedby":"request-status-label"})]}),(0,n.jsxs)(a.Kqy,{children:[(0,n.jsx)(a.lXp,{size:"md",id:"request-action-type-label",children:"Request Type"}),(0,n.jsx)(Z,{options:_.rE,value:x,onChange:s,"aria-describedby":"request-action-type-label"})]})]})}),(0,n.jsxs)(a.mzw,{justifyContent:"space-between",children:[(0,n.jsx)(a.wpx,{type:"text",onClick:u,children:"Clear all"}),(0,n.jsx)(a.wpx,{type:"primary",onClick:t,children:"Done"})]})]})]})},F=e=>{let{...t}=e,{plus:r}=(0,c.hz)(),[l,i]=(0,u.useState)(""),s=(0,f.v9)(b.dp),o=(0,f.v9)(y.rK),d=(0,a.pmc)(),p=(0,m.useRouter)(),g=(0,f.I0)(),{PAGE_SIZES:_,pageSize:C,setPageSize:q,onPreviousPageClick:w,isPreviousPageDisabled:E,onNextPageClick:R,isNextPageDisabled:S,startRange:k,endRange:P,pageIndex:T,setTotalPages:I,resetPageIndexToDefault:A}=(0,j.oi)(),{isOpen:O,onOpen:D,onClose:Z}=(0,a.qY0)(),{data:N,isLoading:F,isFetching:M}=(0,b.QA)({...s,page:T,size:C}),{items:V,total:B}=(0,u.useMemo)(()=>{let e=N||{items:[],total:0,pages:0};return I(e.pages),e},[N,I]),L=(0,u.useCallback)(e=>{g((0,b.mU)(e)),i(e),A()},[g,A,i]),W=async()=>{let e;try{await (0,b.py)({...s,token:o})}catch(t){e=t instanceof Error?t.message:"Unknown error occurred"}e&&d({description:"".concat(e),duration:5e3,status:"error"})},Y=e=>{p.push("/privacy-requests/".concat(e))},G=(0,h.b7)({getCoreRowModel:(0,x.sC)(),data:V,columns:(0,u.useMemo)(()=>z(r),[r]),getRowId:e=>"".concat(e.status,"-").concat(e.id),manualPagination:!0,columnResizeMode:"onChange"});return(0,n.jsxs)(a.xuv,{...t,children:[(0,n.jsxs)(j.Q$,{children:[(0,n.jsx)(j.HO,{globalFilter:l,setGlobalFilter:L,placeholder:"Search by request ID or identity value"}),(0,n.jsxs)(a.Ugi,{alignItems:"center",spacing:4,children:[(0,n.jsx)(a.wpx,{"data-testid":"filter-btn",size:"small",onClick:D,children:"Filter"}),(0,n.jsx)(a.wpx,{"aria-label":"Export report","data-testid":"export-btn",size:"small",icon:(0,n.jsx)(v.nM,{ml:"1.5px"}),onClick:W})]}),(0,n.jsx)(a.h_i,{children:(0,n.jsx)(U,{isOpen:O,onClose:Z,onFilterChange:A})})]}),F?(0,n.jsx)(a.xuv,{p:2,borderWidth:1,children:(0,n.jsx)(j.I4,{rowHeight:26,numRows:10})}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(j.ZK,{tableInstance:G,onRowClick:e=>Y(e.id),onSort:e=>{if(!e){g((0,b.p2)()),A();return}let{id:t,desc:r}=e;g((0,b.PU)(t)),g((0,b.iX)(r?"desc":"asc")),A()}}),(0,n.jsx)(j.s8,{totalRows:B||0,pageSizes:_,setPageSize:q,onPreviousPageClick:w,isPreviousPageDisabled:E||M,onNextPageClick:R,isNextPageDisabled:S||M,startRange:k,endRange:P})]})]})};var M=r(60136),V=r(37440),B=r(16781),L=r(34090),W=r(59389),Y=r(9043);let G=(e,t)=>null==t?void 0:t.find(t=>t.policy_key===e),X=e=>{var t,r;if(!e)return W.Ry().shape({policy_key:W.Z_().required().label("Request type")});let l=e.custom_privacy_request_fields?Object.entries(e.custom_privacy_request_fields).map(e=>{let[t,r]=e;return{[t]:W.Ry().shape({value:r.required&&!r.hidden?W.Z_().required().label(r.label):W.Z_().nullable()})}}).reduce((e,t)=>({...e,...t}),{}):{};return W.Ry().shape({policy_key:W.Z_().required().label("Request type"),identity:W.Ry().shape({email:(null===(t=e.identity_inputs)||void 0===t?void 0:t.email)==="required"?W.Z_().email().required().label("Email address"):W.Z_().nullable(),phone_number:(null===(r=e.identity_inputs)||void 0===r?void 0:r.phone)==="required"?W.Z_().matches(/^\+?[1-9]\d{1,14}$/,"Phone number must be formatted correctly (e.g. 15555555555)").required().label("Phone number"):W.Z_().matches(/^\+?[1-9]\d{1,14}$/,"Phone number must be formatted correctly (e.g. 15555555555)").nullable()}),custom_privacy_request_fields:W.Ry().shape(l)})},K={is_verified:!1,policy_key:"",identity:{}},H=e=>{let{identityInputs:t}=e;return t?(0,n.jsxs)(n.Fragment,{children:[t.email?(0,n.jsx)(Y.j0,{name:"identity.email",label:"User email address",isRequired:"required"===t.email,variant:"stacked"}):null,t.phone?(0,n.jsx)(Y.j0,{name:"identity.phone_number",label:"User phone number",isRequired:"required"===t.phone,variant:"stacked"}):null]}):null},Q=e=>{let{customFieldInputs:t}=e;if(!t)return null;let r=Object.entries(t);return(0,n.jsx)(n.Fragment,{children:r.map(e=>{let[t,r]=e;return(0,n.jsx)(Y.j0,{name:"custom_privacy_request_fields.".concat(t,".value"),label:r.label,isRequired:!!r.required,variant:"stacked"},t)})})};var J=e=>{let{onSubmit:t,onCancel:r}=e,{data:l}=(0,b.xv)();return(0,n.jsx)(L.J9,{initialValues:K,onSubmit:t,validationSchema:()=>(0,W.Vo)(e=>X(G(e.policy_key,null==l?void 0:l.actions))),children:e=>{var t;let{values:i,dirty:s,isValid:o,isSubmitting:d,setFieldValue:u}=e,c=G(i.policy_key,null==l?void 0:l.actions),p=e=>{let t=G(e.value,null==l?void 0:l.actions);if(!(null==t?void 0:t.custom_privacy_request_fields)){u("custom_privacy_request_fields",void 0);return}u("custom_privacy_request_fields",Object.entries(t.custom_privacy_request_fields).map(e=>{let[t,r]=e;return{[t]:{label:r.label,value:r.default_value}}}).reduce((e,t)=>({...e,...t}),{}))};return(0,n.jsx)(L.l0,{children:(0,n.jsxs)(a.Kqy,{spacing:6,mb:2,children:[(0,n.jsx)(Y.AP,{name:"policy_key",label:"Request type",options:null!==(t=null==l?void 0:l.actions.map(e=>({label:e.title,value:e.policy_key})))&&void 0!==t?t:[],onChange:e=>p(e),variant:"stacked",isRequired:!0}),(0,n.jsx)(H,{identityInputs:null==c?void 0:c.identity_inputs}),(0,n.jsx)(Q,{customFieldInputs:null==c?void 0:c.custom_privacy_request_fields}),(0,n.jsx)(Y.Xl,{name:"is_verified",label:"I confirm that I have verified this user information"}),(0,n.jsxs)("div",{className:"flex gap-4 self-end",children:[(0,n.jsx)(a.wpx,{onClick:r,children:"Cancel"}),(0,n.jsx)(a.wpx,{htmlType:"submit",type:"primary",disabled:!i.is_verified||!s||!o,loading:d,"data-testid":"submit-btn",children:"Create"})]})]})})}})},$=r(43073);let ee=e=>{let{isOpen:t,onClose:r}=e,[l]=(0,b.M6)(),i=(0,a.pmc)(),s=async e=>{let{is_verified:t,...n}=e,s=n.custom_privacy_request_fields?Object.entries(n.custom_privacy_request_fields).map(e=>{let[t,r]=e;return r.value?{[t]:r}:{}}).reduce((e,t)=>({...e,...t}),{}):void 0,a={...n,custom_privacy_request_fields:s},o=await l([a]);(0,$.D4)(o)?i((0,B.Vo)((0,M.e$)(o.error,"An error occurred while creating this privacy request. Please try again"))):i((0,B.t5)("Privacy request created")),r()};return(0,n.jsxs)(a.u_l,{isOpen:t,onClose:r,size:"2xl",isCentered:!0,children:[(0,n.jsx)(a.ZAr,{}),(0,n.jsxs)(a.hzk,{"data-testid":"submit-request-modal",maxHeight:"80%",overflowY:"auto",children:[(0,n.jsx)(a.xBx,{children:"Create privacy request"}),(0,n.jsx)(a.fef,{children:(0,n.jsxs)(a.Kqy,{spacing:4,children:[(0,n.jsx)(V.Z,{title:"Warning: You are bypassing identity verification",text:"You are bypassing Fides' built-in identity verification step. Please ensure that you are only entering information on behalf of a verified and approved user's privacy request."}),(0,n.jsx)(J,{onSubmit:s,onCancel:()=>r()})]})})]})]})};var et=()=>{let{onOpen:e,isOpen:t,onClose:r}=(0,a.qY0)();return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(ee,{isOpen:t,onClose:r}),(0,n.jsx)(a.wpx,{type:"primary",size:"small",onClick:e,"data-testid":"submit-request-btn",children:"Create request"})]})},er=r(53359);let el=()=>{let{errorAlert:e}=(0,er.V)(),[t,r]=(0,u.useState)(!1),[l,i]=(0,u.useState)({count:0,total:0}),[s,o]=(0,u.useState)(!0),d=C.q2.ERROR,{data:c}=(0,b.tE)(),{data:p}=(0,b.QA)({status:[d]},{pollingInterval:15e3,skip:s});return(0,u.useEffect)(()=>{o(!(c&&c.notify_after_failures>0))},[c]),(0,u.useEffect)(()=>{let e=(null==p?void 0:p.total)||0;e>=((null==c?void 0:c.notify_after_failures)||0)&&e>l.total?(i({count:e-l.total,total:e}),r(!0)):r(!1)},[null==p?void 0:p.total,null==c?void 0:c.notify_after_failures,l.total]),{processing:()=>{t&&e((0,n.jsxs)(a.xuv,{children:["DSR automation has failed for"," ",(0,n.jsx)(a.xvT,{as:"span",fontWeight:"semibold",children:l.count})," ","privacy request(s). Please review the event log for further details."]}),void 0,{containerStyle:{maxWidth:"max-content"},duration:null,id:"dsrErrorAlert"})}}},ei=d()(()=>r.e(7528).then(r.bind(r,37528)),{loadableGenerated:{webpack:()=>[37528]},loading:()=>(0,n.jsx)("div",{children:"Loading..."})});var en=()=>{let{processing:e}=el(),{plus:t}=(0,c.hz)();return(0,u.useEffect)(()=>{e()},[e]),(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(a.kCb,{"data-testid":"privacy-requests",gap:2,children:[(0,n.jsx)(a.X6q,{mb:8,fontSize:"2xl",fontWeight:"semibold",children:"Privacy Requests"}),(0,n.jsx)(a.LZC,{}),t&&(0,n.jsx)(p.ZP,{scopes:[C.Sh.PRIVACY_REQUEST_CREATE],children:(0,n.jsx)(et,{})}),(0,n.jsx)(ei,{})]}),(0,n.jsx)(F,{})]})},es=()=>(0,n.jsx)(s.Z,{title:"Privacy Requests",mainProps:{px:10},children:(0,n.jsx)(en,{})})},43073:function(e,t,r){"use strict";r.d(t,{Bw:function(){return l.Bw},D4:function(){return l.D4}});var l=r(41164)},23600:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),function(e,t){for(var r in t)Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}(t,{default:function(){return a},noSSR:function(){return s}});let l=r(51538);r(24246),r(27378);let i=l._(r(45362));function n(e){return{default:(null==e?void 0:e.default)||e}}function s(e,t){return delete t.webpack,delete t.modules,e(t)}function a(e,t){let r=i.default,l={loading:e=>{let{error:t,isLoading:r,pastDelay:l}=e;return null}};e instanceof Promise?l.loader=()=>e:"function"==typeof e?l.loader=e:"object"==typeof e&&(l={...l,...e});let a=(l={...l,...t}).loader;return(l.loadableGenerated&&(l={...l,...l.loadableGenerated},delete l.loadableGenerated),"boolean"!=typeof l.ssr||l.ssr)?r({...l,loader:()=>null!=a?a().then(n):Promise.resolve(n(()=>null))}):(delete l.webpack,delete l.modules,s(r,l))}("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},91389:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"LoadableContext",{enumerable:!0,get:function(){return l}});let l=r(51538)._(r(27378)).default.createContext(null)},45362:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return p}});let l=r(51538)._(r(27378)),i=r(91389),n=[],s=[],a=!1;function o(e){let t=e(),r={loading:!0,loaded:null,error:null};return r.promise=t.then(e=>(r.loading=!1,r.loaded=e,e)).catch(e=>{throw r.loading=!1,r.error=e,e}),r}class d{promise(){return this._res.promise}retry(){this._clearTimeouts(),this._res=this._loadFn(this._opts.loader),this._state={pastDelay:!1,timedOut:!1};let{_res:e,_opts:t}=this;e.loading&&("number"==typeof t.delay&&(0===t.delay?this._state.pastDelay=!0:this._delay=setTimeout(()=>{this._update({pastDelay:!0})},t.delay)),"number"==typeof t.timeout&&(this._timeout=setTimeout(()=>{this._update({timedOut:!0})},t.timeout))),this._res.promise.then(()=>{this._update({}),this._clearTimeouts()}).catch(e=>{this._update({}),this._clearTimeouts()}),this._update({})}_update(e){this._state={...this._state,error:this._res.error,loaded:this._res.loaded,loading:this._res.loading,...e},this._callbacks.forEach(e=>e())}_clearTimeouts(){clearTimeout(this._delay),clearTimeout(this._timeout)}getCurrentValue(){return this._state}subscribe(e){return this._callbacks.add(e),()=>{this._callbacks.delete(e)}}constructor(e,t){this._loadFn=e,this._opts=t,this._callbacks=new Set,this._delay=null,this._timeout=null,this.retry()}}function u(e){return function(e,t){let r=Object.assign({loader:null,loading:null,delay:200,timeout:null,webpack:null,modules:null},t),n=null;function o(){if(!n){let t=new d(e,r);n={getCurrentValue:t.getCurrentValue.bind(t),subscribe:t.subscribe.bind(t),retry:t.retry.bind(t),promise:t.promise.bind(t)}}return n.promise()}if(!a){let e=r.webpack?r.webpack():r.modules;e&&s.push(t=>{for(let r of e)if(t.includes(r))return o()})}function u(e,t){!function(){o();let e=l.default.useContext(i.LoadableContext);e&&Array.isArray(r.modules)&&r.modules.forEach(t=>{e(t)})}();let s=l.default.useSyncExternalStore(n.subscribe,n.getCurrentValue,n.getCurrentValue);return l.default.useImperativeHandle(t,()=>({retry:n.retry}),[]),l.default.useMemo(()=>{var t;return s.loading||s.error?l.default.createElement(r.loading,{isLoading:s.loading,pastDelay:s.pastDelay,timedOut:s.timedOut,error:s.error,retry:n.retry}):s.loaded?l.default.createElement((t=s.loaded)&&t.default?t.default:t,e):null},[e,s])}return u.preload=()=>o(),u.displayName="LoadableComponent",l.default.forwardRef(u)}(o,e)}function c(e,t){let r=[];for(;e.length;){let l=e.pop();r.push(l(t))}return Promise.all(r).then(()=>{if(e.length)return c(e,t)})}u.preloadAll=()=>new Promise((e,t)=>{c(n).then(e,t)}),u.preloadReady=e=>(void 0===e&&(e=[]),new Promise(t=>{let r=()=>(a=!0,t());c(s,e).then(r,r)})),window.__NEXT_PRELOADREADY=u.preloadReady;let p=u},65218:function(e,t,r){e.exports=r(23600)}},function(e){e.O(0,[8033,6451,8540,2888,9774,179],function(){return e(e.s=1565)}),_N_E=e.O()}]);