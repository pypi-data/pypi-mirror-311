(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3785],{19785:function(e){var t=Array.isArray;e.exports=t},90988:function(e,t,s){(window.__NEXT_P=window.__NEXT_P||[]).push(["/systems",function(){return s(91903)}])},81836:function(e,t,s){"use strict";var n=s(24246),i=s(27378),r=s(5152),a=s(79894),l=s.n(a);t.Z=e=>{let{breadcrumbs:t,fontSize:s="2xl",fontWeight:a="semibold",separator:o="->",lastItemStyles:c={color:"black"},normalItemStyles:d={color:"gray.500"},...u}=e;return(0,n.jsx)(r.aGc,{separator:o,fontSize:s,fontWeight:a,"data-testid":"breadcrumbs",...u,children:t.map((e,s)=>{let a=s+1===t.length;return e.title?(0,i.createElement)(r.gN6,{...d,...a?c:{},key:e.title,children:[(null==e?void 0:e.icon)&&(0,n.jsx)(r.xuv,{mr:2,children:e.icon}),e.link?(0,n.jsx)(r.Atw,{as:l(),href:e.link,isCurrentPage:a,children:e.title}):(0,n.jsx)(r.Atw,{_hover:{textDecoration:"none",cursor:"default"},isCurrentPage:a,children:e.title})]}):null})})}},79711:function(e,t,s){"use strict";s.d(t,{q:function(){return i}});var n=s(24246);let i=(0,s(5152).IUT)({displayName:"TrashCanOutlineIcon",viewBox:"0 0 11 12",path:(0,n.jsx)("path",{d:"M4.5166 1.60859L4.1084 2.21875H7.22363L6.81543 1.60859C6.7832 1.56133 6.72949 1.53125 6.67148 1.53125H4.6584C4.60039 1.53125 4.54668 1.55918 4.51445 1.60859H4.5166ZM7.6748 1.03711L8.46328 2.21875H8.75977H9.79102H9.96289C10.2486 2.21875 10.4785 2.44863 10.4785 2.73438C10.4785 3.02012 10.2486 3.25 9.96289 3.25H9.79102V9.78125C9.79102 10.7309 9.02188 11.5 8.07227 11.5H3.25977C2.31016 11.5 1.54102 10.7309 1.54102 9.78125V3.25H1.36914C1.0834 3.25 0.853516 3.02012 0.853516 2.73438C0.853516 2.44863 1.0834 2.21875 1.36914 2.21875H1.54102H2.57227H2.86875L3.65723 1.03496C3.88066 0.701953 4.25664 0.5 4.6584 0.5H6.67148C7.07324 0.5 7.44922 0.701953 7.67266 1.03496L7.6748 1.03711ZM2.57227 3.25V9.78125C2.57227 10.1615 2.87949 10.4688 3.25977 10.4688H8.07227C8.45254 10.4688 8.75977 10.1615 8.75977 9.78125V3.25H2.57227ZM4.29102 4.625V9.09375C4.29102 9.28281 4.13633 9.4375 3.94727 9.4375C3.7582 9.4375 3.60352 9.28281 3.60352 9.09375V4.625C3.60352 4.43594 3.7582 4.28125 3.94727 4.28125C4.13633 4.28125 4.29102 4.43594 4.29102 4.625ZM6.00977 4.625V9.09375C6.00977 9.28281 5.85508 9.4375 5.66602 9.4375C5.47695 9.4375 5.32227 9.28281 5.32227 9.09375V4.625C5.32227 4.43594 5.47695 4.28125 5.66602 4.28125C5.85508 4.28125 6.00977 4.43594 6.00977 4.625ZM7.72852 4.625V9.09375C7.72852 9.28281 7.57383 9.4375 7.38477 9.4375C7.1957 9.4375 7.04102 9.28281 7.04102 9.09375V4.625C7.04102 4.43594 7.1957 4.28125 7.38477 4.28125C7.57383 4.28125 7.72852 4.43594 7.72852 4.625Z",fill:"currentColor"})})},43124:function(e,t,s){"use strict";s.d(t,{Z:function(){return x}});var n=s(24246),i=s(5152),r=s(88038),a=s.n(r),l=s(86677);s(27378);var o=s(11596),c=s(72247),d=s(11032),u=()=>{let e=(0,l.useRouter)();return(0,n.jsx)(i.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,n.jsxs)(i.xuv,{children:[(0,n.jsxs)(i.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,n.jsx)(i.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,n.jsx)(i.wpx,{onClick:()=>{e.push(d.fz)},children:"Configure"})]}),(0,n.jsxs)(i.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},x=e=>{let{children:t,title:s,padded:r=!0,mainProps:d}=e,x=(0,o.hz)(),m=(0,l.useRouter)(),h="/privacy-requests"===m.pathname||"/datastore-connection"===m.pathname,p=!(x.flags.privacyRequestsConfiguration&&h),{data:g}=(0,c.JE)(void 0,{skip:p}),{data:f}=(0,c.PW)(void 0,{skip:p}),j=x.flags.privacyRequestsConfiguration&&(!g||!f)&&h;return(0,n.jsxs)(i.kCb,{"data-testid":s,direction:"column",h:"100vh",children:[(0,n.jsxs)(a(),{children:[(0,n.jsxs)("title",{children:["Fides Admin UI - ",s]}),(0,n.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,n.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,n.jsxs)(i.kCb,{as:"main",direction:"column",py:r?6:0,px:r?10:0,h:r?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...d,children:[j?(0,n.jsx)(u,{}):null,t]})]})}},37541:function(e,t,s){"use strict";var n=s(24246),i=s(5152),r=s(19785),a=s.n(r),l=s(27378),o=s(81836);t.Z=e=>{let{breadcrumbs:t,isSticky:s=!0,children:r,rightContent:c,...d}=e;return(0,n.jsxs)(i.xuv,{bgColor:"white",paddingY:5,...s?{position:"sticky",top:0,left:0,zIndex:10}:{},...d,children:[(0,n.jsxs)(i.kCb,{alignItems:"flex-start",children:[(0,n.jsxs)(i.xuv,{flex:1,children:[a()(t)&&(0,n.jsx)(i.xuv,{marginBottom:r?4:0,children:(0,n.jsx)(o.Z,{breadcrumbs:t})}),(0,l.isValidElement)(t)&&t]}),c&&(0,n.jsx)(i.xuv,{children:c})]}),r]})}},38615:function(e,t,s){"use strict";s.d(t,{Tg:function(){return a}});var n=s(24246),i=s(44296),r=s(96451);let a=e=>(0,i.C)(r.uu).filter(t=>e.includes(t)).length>0;t.ZP=e=>{let{scopes:t,children:s}=e;return a(t)?(0,n.jsx)(n.Fragment,{children:s}):null}},91903:function(e,t,s){"use strict";s.r(t);var n=s(24246),i=s(92222),r=s(59003),a=s(5152),l=s(86677),o=s(27378),c=s(44296),d=s(60136),u=s(79711),x=s(43124),m=s(11032),h=s(37541),p=s(38615),g=s(8540),f=s(16781),j=s(22153),C=s(10284),v=s(43073);let y=(0,i.Cl)(),b={items:[],total:0,page:1,size:25,pages:1},w=()=>(0,n.jsxs)(a.gCW,{mt:6,p:10,spacing:4,borderRadius:"base",maxW:"70%","data-testid":"no-results-notice",alignSelf:"center",margin:"auto",textAlign:"center",children:[(0,n.jsxs)(a.gCW,{children:[(0,n.jsx)(a.xvT,{fontSize:"md",fontWeight:"600",children:"No systems found."}),(0,n.jsx)(a.xvT,{fontSize:"sm",children:'Click "Add a system" to add your first system to Fides.'})]}),(0,n.jsx)(a.wpx,{href:m.xo,size:"small",type:"primary","data-testid":"add-privacy-notice-btn",children:"Add a system +"})]});t.default=()=>{let e=(0,l.useRouter)(),t=(0,c.T)(),s=(0,a.pmc)(),{isOpen:k,onOpen:_,onClose:R}=(0,a.qY0)(),[P]=(0,j.DW)(),[z,S]=o.useState(null),{PAGE_SIZES:H,pageSize:T,setPageSize:V,onPreviousPageClick:E,isPreviousPageDisabled:N,onNextPageClick:Z,isNextPageDisabled:D,startRange:M,endRange:A,pageIndex:F,setTotalPages:W,resetPageIndexToDefault:q}=(0,g.oi)(),[I,L]=(0,o.useState)(),O=(0,o.useCallback)(e=>{q(),L(e)},[q,L]),{data:G,isLoading:Y,isFetching:B}=(0,j.xF)({page:F,size:T,search:I}),{items:U,total:K,pages:Q}=(0,o.useMemo)(()=>null!=G?G:b,[G]);(0,o.useEffect)(()=>{W(Q)},[Q,W]);let X=e=>e.name&&""!==e.name?e.name:e.fides_key,$=(0,o.useCallback)(s=>{t((0,j.db)(s)),e.push({pathname:m.Dv,query:{id:s.fides_key}})},[t,e]),J=async e=>{let t=await P(e.fides_key);(0,v.D4)(t)?s((0,f.Vo)((0,d.e$)(t.error))):s((0,f.t5)("Successfully deleted system")),R()},ee=(0,o.useMemo)(()=>[y.accessor(e=>e.name,{id:"name",cell:e=>(0,n.jsx)(g.G3,{value:X(e.row.original)}),header:e=>(0,n.jsx)(g.Rr,{value:"System Name",...e}),size:200}),y.accessor(e=>e.description,{id:"description",header:e=>(0,n.jsx)(g.Rr,{value:"Description",...e}),cell:e=>(0,n.jsx)(g.G3,{value:e.getValue(),cellProps:e}),size:300,meta:{showHeaderMenu:!0}}),y.accessor(e=>e.administrating_department,{id:"department",cell:e=>(0,n.jsx)(g.G3,{value:e.getValue()}),header:e=>(0,n.jsx)(g.Rr,{value:"Department",...e}),size:200}),y.accessor(e=>e.processes_personal_data,{id:"processes_personal_data",cell:e=>(0,n.jsx)(g.G3,{value:e.getValue()?"Yes":"No"}),header:e=>(0,n.jsx)(g.Rr,{value:"Processes Personal Data",...e}),size:100}),y.display({id:"actions",header:"Actions",cell:e=>{let{row:t}=e,s=t.original;return(0,n.jsxs)(a.Ugi,{spacing:0,"data-testid":"system-".concat(s.fides_key),children:[(0,n.jsx)(a.wpx,{"aria-label":"Edit property","data-testid":"edit-btn",size:"small",className:"mr-2",icon:(0,n.jsx)(a.dY8,{}),onClick:()=>$(s)}),(0,n.jsx)(p.ZP,{scopes:[C.Sh.SYSTEM_DELETE],children:(0,n.jsx)(a.wpx,{"aria-label":"Delete system","data-testid":"delete-btn",size:"small",className:"mr-2",icon:(0,n.jsx)(u.q,{}),onClick:()=>{S(s),_()}})})]})},meta:{disableRowClick:!0}})],[$,_]),et=(0,r.b7)({getCoreRowModel:(0,i.sC)(),getFilteredRowModel:(0,i.vL)(),getSortedRowModel:(0,i.tj)(),columnResizeMode:"onChange",columns:ee,data:U});return(0,n.jsx)(x.Z,{title:"System inventory",mainProps:{paddingTop:0},children:(0,n.jsxs)(a.xuv,{"data-testid":"system-management",children:[(0,n.jsx)(h.Z,{breadcrumbs:[{title:"System inventory"}],children:(0,n.jsx)(a.xvT,{fontSize:"sm",mb:1,children:"View and manage recently detected systems and vendors here."})}),Y?(0,n.jsx)(g.I4,{rowHeight:36,numRows:15}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(g.Q$,{children:(0,n.jsx)(g.HO,{globalFilter:I,setGlobalFilter:O,placeholder:"Search",testid:"system-search"})}),(0,n.jsx)(g.ZK,{tableInstance:et,emptyTableNotice:(0,n.jsx)(w,{}),onRowClick:$})]}),(0,n.jsx)(g.s8,{totalRows:K||0,pageSizes:H,setPageSize:V,onPreviousPageClick:E,isPreviousPageDisabled:N||B,onNextPageClick:Z,isNextPageDisabled:D||B,startRange:M,endRange:A}),(0,n.jsx)(a.cVQ,{isOpen:k,onClose:R,onConfirm:()=>J(z),title:"Delete ".concat(z&&X(z)),message:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(a.xvT,{children:["You are about to permanently delete the system"," ",(0,n.jsx)(a.xvT,{color:"complimentary.500",as:"span",fontWeight:"bold",whiteSpace:"nowrap",children:z&&X(z)}),"."]}),(0,n.jsx)(a.xvT,{children:"Are you sure you would like to continue?"})]})})]})})}},43073:function(e,t,s){"use strict";s.d(t,{Bw:function(){return n.Bw},D4:function(){return n.D4}});var n=s(41164)}},function(e){e.O(0,[8033,6451,8540,2888,9774,179],function(){return e(e.s=90988)}),_N_E=e.O()}]);