(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3709],{54727:function(e,s,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/consent/configure",function(){return n(58875)}])},56901:function(e,s,n){"use strict";n.d(s,{ZS:function(){return o},a4:function(){return l}});var t=n(80406);let i=n(21618).u.injectEndpoints({endpoints:e=>({getPurposes:e.query({query:()=>"purposes"})})}),{useGetPurposesQuery:l}=i,a={purposes:{},special_purposes:{}},o=(0,t.P1)(i.endpoints.getPurposes.select(),e=>{let{data:s}=e;return s||a})},58875:function(e,s,n){"use strict";n.r(s),n.d(s,{default:function(){return R}});var t=n(24246),i=n(5152),l=n(27378),a=n(43124),o=n(92222),r=n(59003),c=n(11596),u=n(8540),d=n(86677);let x=(e,s)=>{let n=e.filter(e=>e.isChecked);return n.length>0?"".concat(s,"=").concat(n.map(e=>e.value).join("&".concat(s,"="))):void 0},p=e=>{let{value:s,displayText:n,isChecked:l,onCheckboxChange:a}=e;return(0,t.jsx)(i.XZJ,{value:s,height:"20px",mb:"25px",isChecked:l,onChange:e=>{let{target:n}=e;a(s,n.checked)},_focusWithin:{bg:"gray.100"},colorScheme:"complimentary",children:(0,t.jsx)(i.xvT,{fontSize:"sm",lineHeight:5,textOverflow:"ellipsis",overflow:"hidden",children:n})},s)},h=e=>{let{options:s,header:n,onCheckboxChange:a,columns:o=3,numDefaultOptions:r=15}=e,[c,u]=(0,l.useState)(!1),d=c?s:s.slice(0,r),x=s.length>r;return(0,t.jsxs)(i.Qdk,{border:"0px",padding:"12px 8px 8px 12px",children:[(0,t.jsx)(i.X6q,{height:"56px",children:(0,t.jsxs)(i.KFZ,{height:"100%",children:[(0,t.jsx)(i.xuv,{flex:"1",alignItems:"center",justifyContent:"center",textAlign:"left",fontWeight:600,children:n}),(0,t.jsx)(i.XEm,{})]})}),(0,t.jsxs)(i.Hk3,{id:"panel-".concat(n),children:[(0,t.jsx)(i.MIq,{columns:o,children:d.map(e=>(0,t.jsx)(p,{...e,onCheckboxChange:a},e.value))}),!c&&x?(0,t.jsx)(i.wpx,{type:"text",onClick:()=>{u(!0)},children:"View more"}):null,c&&x?(0,t.jsx)(i.wpx,{type:"text",onClick:()=>{u(!1)},children:"View less"}):null]})]})},g=e=>{let{heading:s,children:n}=e;return(0,t.jsxs)(i.xuv,{padding:"12px 8px 8px 12px",maxHeight:600,children:[s?(0,t.jsx)(i.X6q,{size:"md",lineHeight:6,fontWeight:"bold",mb:2,children:s}):null,n]})},j=e=>{let{resetFilters:s,isOpen:n,onClose:l,children:a,...o}=e;return(0,t.jsxs)(i.u_l,{isOpen:n,onClose:l,isCentered:!0,size:"2xl",...o,children:[(0,t.jsx)(i.ZAr,{}),(0,t.jsxs)(i.hzk,{children:[(0,t.jsx)(i.xBx,{children:"Filters"}),(0,t.jsx)(i.olH,{}),(0,t.jsx)(i.izJ,{}),(0,t.jsx)(i.fef,{maxH:"85vh",padding:"0px",overflowX:"auto",style:{scrollbarGutter:"stable"},children:a}),(0,t.jsx)(i.mzw,{children:(0,t.jsxs)(i.xuv,{display:"flex",justifyContent:"space-between",width:"100%",children:[(0,t.jsx)(i.wpx,{onClick:s,className:"mr-3 grow",children:"Reset filters"}),(0,t.jsx)(i.wpx,{type:"primary",onClick:l,className:"grow",children:"Done"})]})})]})]})};var C=n(11032),m=n(85815),f=n(44296),b=n(56901),v=n(79851);let k=()=>{let{isOpen:e,onClose:s,onOpen:n}=(0,i.qY0)();(0,v.fd)();let t=(0,f.C)(v.U3);(0,b.a4)();let a=(0,f.C)(b.ZS),[o,r]=(0,l.useState)([]),[c,u]=(0,l.useState)([]),[d,x]=(0,l.useState)([{displayText:"Consent",value:"Consent",isChecked:!1},{displayText:"Legitimate Interest",value:"Legitimate interests",isChecked:!1}]),[p,h]=(0,l.useState)([{displayText:"Advertising",value:"advertising",isChecked:!1},{displayText:"Analytics",value:"analytics",isChecked:!1},{displayText:"Functional",value:"functional",isChecked:!1},{displayText:"Essential",value:"essential",isChecked:!1}]);(0,l.useEffect)(()=>{0===c.length&&u(t.map(e=>({value:e.fides_key,displayText:e.name||e.fides_key,isChecked:!1})))},[t,c,u]),(0,l.useEffect)(()=>{0===o.length&&r([...Object.entries(a.purposes).map(e=>({value:"normal.".concat(e[0]),displayText:e[1].name,isChecked:!1})),...Object.entries(a.special_purposes).map(e=>({value:"special.".concat(e[0]),displayText:e[1].name,isChecked:!1}))])},[a,o,u]);let g=(e,s,n,t)=>{t(n.map(n=>n.value===e?{...n,isChecked:s}:n))};return{isOpen:e,onClose:s,onOpen:n,resetFilters:()=>{u(e=>e.map(e=>({...e,isChecked:!1}))),x(e=>e.map(e=>({...e,isChecked:!1}))),r(e=>e.map(e=>({...e,isChecked:!1}))),h(e=>e.map(e=>({...e,isChecked:!1})))},purposeOptions:o,onPurposeChange:(e,s)=>{g(e,s,o,r)},dataUseOptions:c,onDataUseChange:(e,s)=>{g(e,s,c,u)},legalBasisOptions:d,onLegalBasisChange:(e,s)=>{g(e,s,d,x)},consentCategoryOptions:p,onConsentCategoryChange:(e,s)=>{g(e,s,p,h)}}},y=e=>{let{isOpen:s,isTcfEnabled:n,onClose:l,resetFilters:a,purposeOptions:o,onPurposeChange:r,dataUseOptions:c,onDataUseChange:u,legalBasisOptions:d,onLegalBasisChange:x,consentCategoryOptions:p,onConsentCategoryChange:C}=e;return(0,t.jsx)(j,{isOpen:s,onClose:l,resetFilters:a,children:(0,t.jsx)(i.UQy,{children:(0,t.jsxs)(g,{children:[n?(0,t.jsx)(h,{options:o,onCheckboxChange:r,header:"TCF purposes",columns:1,numDefaultOptions:5}):null,(0,t.jsx)(h,{options:c,onCheckboxChange:u,header:"Data uses"}),n?(0,t.jsx)(h,{options:d,onCheckboxChange:x,header:"Legal basis"}):null,n?null:(0,t.jsx)(h,{options:p,onCheckboxChange:C,header:"Consent categories"})]})})})};var _=n(34090),w=n(9043),S=n(96878);let O=()=>{let{isOpen:e,onOpen:s,onClose:n}=(0,i.qY0)();return{isOpen:e,onOpen:s,onClose:n}},z=e=>{let{isOpen:s,onClose:n,fidesKey:l}=e,{data:a,isLoading:o}=(0,S.ho)(l);return(0,t.jsxs)(i.u_l,{isOpen:s,onClose:n,size:"xxl",returnFocusOnClose:!1,isCentered:!0,children:[(0,t.jsx)(i.ZAr,{}),(0,t.jsxs)(i.hzk,{maxWidth:"800px",children:[(0,t.jsx)(i.xBx,{children:"Vendor"}),(0,t.jsx)(i.fef,{children:o?(0,t.jsx)(i.kCb,{width:"100%",height:"324px",alignItems:"center",justifyContent:"center",children:(0,t.jsx)(i.$jN,{})}):(0,t.jsx)(_.J9,{initialValues:a,enableReinitialize:!0,onSubmit:()=>{},children:e=>{let{values:s}=e;return(0,t.jsxs)(_.l0,{children:[(0,t.jsx)(i.xuv,{mb:6,children:(0,t.jsx)(w.j0,{label:"Vendor Name",variant:"stacked",name:"name",disabled:!0})}),Object.entries((null==s?void 0:s.purposes)||{}).length>0?(0,t.jsx)(w.__,{children:" Purposes "}):null,(0,t.jsx)(_.F2,{name:"purposes",render:()=>(0,t.jsx)(i.UQy,{allowMultiple:!0,children:Object.entries(s.purposes).map((e,s)=>{let[n]=e;return(0,t.jsx)(i.Qdk,{children:e=>{let{isExpanded:s}=e;return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsxs)(i.KFZ,{backgroundColor:s?"gray.50":"unset",children:[(0,t.jsx)(i.xuv,{flex:"1",textAlign:"left",children:n}),(0,t.jsx)(i.XEm,{})]}),(0,t.jsxs)(i.Hk3,{backgroundColor:"gray.50",children:[(0,t.jsx)(i.xuv,{my:4,children:(0,t.jsx)(w.VT,{label:"Data Uses",isMulti:!0,disableMenu:!0,isDisabled:!0,options:[],variant:"stacked",name:"purposes['".concat(n,"'].data_uses")})}),(0,t.jsx)(w.VT,{label:"Legal Basis",isMulti:!0,disableMenu:!0,isDisabled:!0,options:[],variant:"stacked",name:"purposes['".concat(n,"'].legal_bases")})]})]})}},s)})})}),(0,t.jsx)(i.xuv,{my:4,children:(0,t.jsx)(w.VT,{label:"Features",isMulti:!0,options:[],disableMenu:!0,isDisabled:!0,variant:"stacked",name:"features"})}),(0,t.jsx)(w.VT,{label:"Data Categories",isMulti:!0,options:[],disableMenu:!0,isDisabled:!0,variant:"stacked",name:"data_categories"})]})}})}),(0,t.jsxs)(i.mzw,{children:[(0,t.jsxs)(i.wpx,{size:"small",onClick:n,children:["Close"," "]}),(0,t.jsx)(i.LZC,{})]})]})]})},M=(0,o.Cl)(),T={items:[],total:0,page:1,size:25,pages:1},F=()=>{let{tcf:e,dictionaryService:s}=(0,c.hz)(),{isLoading:n}=(0,S.x8)(),{isOpen:a,onOpen:p,onClose:h}=O(),g=(0,d.useRouter)(),[j,f]=(0,l.useState)(),{isOpen:b,onOpen:v,onClose:_,resetFilters:w,purposeOptions:F,onPurposeChange:P,dataUseOptions:R,onDataUseChange:V,legalBasisOptions:D,onLegalBasisChange:E,consentCategoryOptions:I,onConsentCategoryChange:L}=k(),N=(0,l.useMemo)(()=>x(R,"data_uses"),[R]),Z=(0,l.useMemo)(()=>x(D,"legal_bases"),[D]),U=(0,l.useMemo)(()=>x(F.filter(e=>e.value.includes("normal")).map(e=>({...e,value:e.value.split(".")[1]})),"purposes"),[F]),H=(0,l.useMemo)(()=>x(F.filter(e=>e.value.includes("special")).map(e=>({...e,value:e.value.split(".")[1]})),"special_purposes"),[F]),X=(0,l.useMemo)(()=>x(I,"consent_category"),[I]),{PAGE_SIZES:q,pageSize:B,setPageSize:A,onPreviousPageClick:Q,isPreviousPageDisabled:W,onNextPageClick:G,isNextPageDisabled:K,startRange:J,endRange:Y,pageIndex:$,setTotalPages:ee,resetPageIndexToDefault:es}=(0,u.oi)(),[en,et]=(0,l.useState)(),ei=(0,l.useCallback)(e=>{es(),et(e)},[es,et]),{isFetching:el,isLoading:ea,data:eo}=(0,S.de)({pageIndex:$,pageSize:B,dataUses:N,search:en,legalBasis:Z,purposes:U,specialPurposes:H,consentCategories:X}),{items:er,total:ec,pages:eu}=(0,l.useMemo)(()=>eo||T,[eo]);(0,l.useEffect)(()=>{ee(eu)},[eu,ee]);let ed=(0,l.useMemo)(()=>[M.accessor(e=>e.name,{id:"name",cell:e=>(0,t.jsx)(u.G3,{value:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"Vendor",...e})}),M.accessor(e=>e.data_uses,{id:"tcf_purpose",cell:e=>(0,t.jsx)(u.CI,{plSuffix:"purposes",singSuffix:"purpose",count:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"TCF purpose",...e})}),M.accessor(e=>e.data_uses,{id:"data_uses",cell:e=>(0,t.jsx)(u.CI,{plSuffix:"data uses",singSuffix:"data use",count:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"Data use",...e})}),M.accessor(e=>e.legal_bases,{id:"legal_bases",cell:e=>(0,t.jsx)(u.CI,{plSuffix:"bases",singSuffix:"basis",count:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"Legal basis",...e})}),M.accessor(e=>e.consent_categories,{id:"consent_categories",cell:e=>(0,t.jsx)(u.CI,{plSuffix:"categories",singSuffix:"category",count:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"Categories",...e})}),M.accessor(e=>e.cookies,{id:"cookies",cell:e=>(0,t.jsx)(u.CI,{plSuffix:"cookies",singSuffix:"cookie",count:e.getValue()}),header:e=>(0,t.jsx)(u.Rr,{value:"Cookies",...e})})],[]),ex=(0,r.b7)({columns:ed,data:er,state:{columnVisibility:{tcf_purpose:e,data_uses:e,legal_bases:e,consent_categories:!e,cookies:!e}},getCoreRowModel:(0,o.sC)(),columnResizeMode:"onChange",enableColumnResizing:!0});return ea||n?(0,t.jsx)(u.I4,{rowHeight:36,numRows:15}):(0,t.jsxs)(i.kCb,{flex:1,direction:"column",overflow:"auto",children:[a&&j?(0,t.jsx)(z,{isOpen:a,fidesKey:j,onClose:h}):null,(0,t.jsxs)(u.Q$,{children:[(0,t.jsx)(u.HO,{globalFilter:en,setGlobalFilter:ei,placeholder:"Search"}),(0,t.jsx)(y,{isOpen:b,isTcfEnabled:e,onClose:_,resetFilters:w,purposeOptions:F,onPurposeChange:P,dataUseOptions:R,onDataUseChange:V,legalBasisOptions:D,onLegalBasisChange:E,consentCategoryOptions:I,onConsentCategoryChange:L}),(0,t.jsxs)(i.Ugi,{alignItems:"center",spacing:4,children:[(0,t.jsx)(m.Z,{buttonLabel:"Add vendors",buttonProps:{size:"small"},onButtonClick:s?()=>{g.push(C.Gg)}:void 0}),(0,t.jsx)(i.wpx,{onClick:v,"data-testid":"filter-multiple-systems-btn",size:"small",children:"Filter"})]})]}),(0,t.jsx)(u.ZK,{tableInstance:ex,onRowClick:e=>{f(e.fides_key),p()}}),(0,t.jsx)(u.s8,{totalRows:ec||0,pageSizes:q,setPageSize:A,onPreviousPageClick:Q,isPreviousPageDisabled:W||el,onNextPageClick:G,isNextPageDisabled:K||el,startRange:J,endRange:Y})]})},P=e=>{let{title:s,description:n}=e;return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(i.xuv,{mb:4,children:(0,t.jsx)(i.X6q,{fontSize:"2xl",fontWeight:"semibold",mb:2,"data-testid":"header",children:s})}),(0,t.jsx)(i.kCb,{children:(0,t.jsx)(i.xvT,{fontSize:"sm",mb:8,width:{base:"100%",lg:"50%"},children:n})})]})};var R=()=>(0,t.jsxs)(a.Z,{title:"Configure consent",children:[(0,t.jsx)(P,{title:"Manage your vendors",description:"Use the table below to manage your vendors. Modify the legal basis for a vendor if permitted and view and group your views by applying different filters"}),(0,t.jsx)(F,{})]})}},function(e){e.O(0,[8033,6451,8540,8141,5815,2888,9774,179],function(){return e(e.s=54727)}),_N_E=e.O()}]);