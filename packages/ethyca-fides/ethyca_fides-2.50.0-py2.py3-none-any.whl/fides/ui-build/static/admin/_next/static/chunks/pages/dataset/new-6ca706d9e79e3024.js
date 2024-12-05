(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8538],{19785:function(e){var t=Array.isArray;e.exports=t},73846:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/dataset/new",function(){return r(95327)}])},81836:function(e,t,r){"use strict";var n=r(24246),s=r(27378),i=r(5152),a=r(79894),l=r.n(a);t.Z=e=>{let{breadcrumbs:t,fontSize:r="2xl",fontWeight:a="semibold",separator:o="->",lastItemStyles:c={color:"black"},normalItemStyles:d={color:"gray.500"},...u}=e;return(0,n.jsx)(i.aGc,{separator:o,fontSize:r,fontWeight:a,"data-testid":"breadcrumbs",...u,children:t.map((e,r)=>{let a=r+1===t.length;return e.title?(0,s.createElement)(i.gN6,{...d,...a?c:{},key:e.title,children:[(null==e?void 0:e.icon)&&(0,n.jsx)(i.xuv,{mr:2,children:e.icon}),e.link?(0,n.jsx)(i.Atw,{as:l(),href:e.link,isCurrentPage:a,children:e.title}):(0,n.jsx)(i.Atw,{_hover:{textDecoration:"none",cursor:"default"},isCurrentPage:a,children:e.title})]}):null})})}},43124:function(e,t,r){"use strict";r.d(t,{Z:function(){return f}});var n=r(24246),s=r(5152),i=r(88038),a=r.n(i),l=r(86677);r(27378);var o=r(11596),c=r(72247),d=r(11032),u=()=>{let e=(0,l.useRouter)();return(0,n.jsx)(s.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,n.jsxs)(s.xuv,{children:[(0,n.jsxs)(s.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,n.jsx)(s.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,n.jsx)(s.wpx,{onClick:()=>{e.push(d.fz)},children:"Configure"})]}),(0,n.jsxs)(s.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},f=e=>{let{children:t,title:r,padded:i=!0,mainProps:d}=e,f=(0,o.hz)(),h=(0,l.useRouter)(),x="/privacy-requests"===h.pathname||"/datastore-connection"===h.pathname,g=!(f.flags.privacyRequestsConfiguration&&x),{data:m}=(0,c.JE)(void 0,{skip:g}),{data:p}=(0,c.PW)(void 0,{skip:g}),y=f.flags.privacyRequestsConfiguration&&(!m||!p)&&x;return(0,n.jsxs)(s.kCb,{"data-testid":r,direction:"column",h:"100vh",children:[(0,n.jsxs)(a(),{children:[(0,n.jsxs)("title",{children:["Fides Admin UI - ",r]}),(0,n.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,n.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,n.jsxs)(s.kCb,{as:"main",direction:"column",py:i?6:0,px:i?10:0,h:i?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...d,children:[y?(0,n.jsx)(u,{}):null,t]})]})}},37541:function(e,t,r){"use strict";var n=r(24246),s=r(5152),i=r(19785),a=r.n(i),l=r(27378),o=r(81836);t.Z=e=>{let{breadcrumbs:t,isSticky:r=!0,children:i,rightContent:c,...d}=e;return(0,n.jsxs)(s.xuv,{bgColor:"white",paddingY:5,...r?{position:"sticky",top:0,left:0,zIndex:10}:{},...d,children:[(0,n.jsxs)(s.kCb,{alignItems:"flex-start",children:[(0,n.jsxs)(s.xuv,{flex:1,children:[a()(t)&&(0,n.jsx)(s.xuv,{marginBottom:i?4:0,children:(0,n.jsx)(o.Z,{breadcrumbs:t})}),(0,l.isValidElement)(t)&&t]}),c&&(0,n.jsx)(s.xuv,{children:c})]}),i]})}},60136:function(e,t,r){"use strict";r.d(t,{D4:function(){return i.D4},MM:function(){return f},Ot:function(){return c},c6:function(){return s},cj:function(){return x},e$:function(){return l},fn:function(){return o},iC:function(){return h},nU:function(){return u},tB:function(){return d}});var n,s,i=r(41164);let a="An unexpected error occurred. Please try again.",l=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:a;if((0,i.Bw)(e)){if((0,i.hE)(e.data))return e.data.detail;if((0,i.cz)(e.data)){var r;let t=null===(r=e.data.detail)||void 0===r?void 0:r[0];return"".concat(null==t?void 0:t.msg,": ").concat(null==t?void 0:t.loc)}if(409===e.status&&(0,i.Dy)(e.data)||404===e.status&&(0,i.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function o(e){return"object"==typeof e&&null!=e&&"status"in e}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function d(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let u=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:a};if((0,i.oK)(e))return{status:e.originalStatus,message:e.data};if((0,i.Bw)(e)){let{status:r}=e;return{status:r,message:l(e,t.message)}}return t},f=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(n=s||(s={})).GVL="gvl",n.AC="gacp",n.COMPASS="compass";let h={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},x=e=>{let t=e.split(".")[0];return"gacp"===t?"gacp":"gvl"===t?"gvl":"compass"}},53359:function(e,t,r){"use strict";r.d(t,{H:function(){return i},V:function(){return n.V}});var n=r(75139),s=r(60136);let i=()=>{let{errorAlert:e}=(0,n.V)();return{handleError:t=>{let r="An unexpected error occurred. Please try again.";(0,s.Ot)(t)?r=t.data.detail:(0,s.tB)(t)&&(r=t.data.detail[0].msg),e(r)}}}},75139:function(e,t,r){"use strict";r.d(t,{V:function(){return i}});var n=r(24246),s=r(5152);let i=()=>{let e=(0,s.pmc)();return{errorAlert:(t,r,i)=>{let a={...i,position:(null==i?void 0:i.position)||"top",render:e=>{let{onClose:i}=e;return(0,n.jsxs)(s.bZj,{alignItems:"normal",status:"error",children:[(0,n.jsx)(s.zMQ,{}),(0,n.jsxs)(s.xuv,{children:[r&&(0,n.jsx)(s.CdC,{children:r}),(0,n.jsx)(s.XaZ,{children:t})]}),(0,n.jsx)(s.PZ7,{onClick:i,position:"relative",right:0,size:"sm",top:-1})]})}};(null==i?void 0:i.id)&&e.isActive(i.id)?e.update(i.id,a):e(a)},successAlert:(t,r,i)=>{let a={...i,position:(null==i?void 0:i.position)||"top",render:e=>{let{onClose:i}=e;return(0,n.jsxs)(s.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,n.jsx)(s.zMQ,{}),(0,n.jsxs)(s.xuv,{children:[r&&(0,n.jsx)(s.CdC,{children:r}),(0,n.jsx)(s.XaZ,{children:t})]}),(0,n.jsx)(s.PZ7,{onClick:i,position:"relative",right:0,size:"sm",top:-1})]})}};(null==i?void 0:i.id)&&e.isActive(i.id)?e.update(i.id,a):e(a)}}}},77650:function(e,t,r){"use strict";var n=r(24246),s=r(5152);t.Z=e=>{let{isOpen:t,onClose:r,onConfirm:i,onCancel:a,title:l,message:o,cancelButtonText:c,continueButtonText:d,isLoading:u,returnFocusOnClose:f,isCentered:h,testId:x="confirmation-modal",icon:g}=e;return(0,n.jsxs)(s.u_l,{isOpen:t,onClose:r,size:"lg",returnFocusOnClose:null==f||f,isCentered:h,children:[(0,n.jsx)(s.ZAr,{}),(0,n.jsxs)(s.hzk,{textAlign:"center",p:6,"data-testid":x,children:[g?(0,n.jsx)(s.M5Y,{mb:2,children:g}):null,l?(0,n.jsx)(s.xBx,{fontWeight:"medium",pb:0,children:l}):null,o?(0,n.jsx)(s.fef,{children:o}):null,(0,n.jsx)(s.mzw,{children:(0,n.jsxs)(s.MIq,{columns:2,width:"100%",children:[(0,n.jsx)(s.wpx,{onClick:()=>{a&&a(),r()},size:"large",className:"mr-3","data-testid":"cancel-btn",disabled:u,children:c||"Cancel"}),(0,n.jsx)(s.wpx,{type:"primary",size:"large",onClick:i,"data-testid":"continue-btn",loading:u,children:d||"Continue"})]})})]})]})}},16781:function(e,t,r){"use strict";r.d(t,{MA:function(){return l},Vo:function(){return c},t5:function(){return o}});var n=r(24246),s=r(5152);let i=e=>{let{children:t}=e;return(0,n.jsxs)(s.xvT,{"data-testid":"toast-success-msg",children:[(0,n.jsx)("strong",{children:"Success:"})," ",t]})},a=e=>{let{children:t}=e;return(0,n.jsxs)(s.xvT,{"data-testid":"toast-error-msg",children:[(0,n.jsx)("strong",{children:"Error:"})," ",t]})},l={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},o=e=>{let t=(0,n.jsx)(i,{children:e});return{...l,description:t}},c=e=>{let t=(0,n.jsx)(a,{children:e});return{...l,description:t,status:"error"}}},50558:function(e,t,r){"use strict";var n=r(24246),s=r(5152);r(27378),t.Z=e=>{let{isEmptyState:t,yamlError:r}=e;return(0,n.jsx)(s.Rg9,{in:!0,children:(0,n.jsxs)(s.xuv,{w:"fit-content",bg:"white",p:3,borderRadius:3,children:[(0,n.jsxs)(s.Ugi,{children:[(0,n.jsx)(s.X6q,{as:"h5",color:"gray.700",size:"xs",children:"YAML"}),(0,n.jsx)(s.Vp9,{colorScheme:"red",size:"sm",variant:"solid",children:"Error"})]}),(0,n.jsx)(s.xuv,{bg:"red.50",border:"1px solid",borderColor:"red.300",color:"red.300",mt:"16px",borderRadius:"6px",children:(0,n.jsxs)(s.Ugi,{alignItems:"flex-start",margin:["14px","17px","14px","17px"],children:[(0,n.jsx)(s.f9v,{}),t&&(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{as:"h5",color:"red.500",fontWeight:"semibold",size:"xs",children:"Error message:"}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:"Yaml system is required"})]}),r&&(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{as:"h5",color:"red.500",fontWeight:"semibold",size:"xs",children:"Error message:"}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:r.message}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:r.reason}),(0,n.jsxs)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:["Ln ",(0,n.jsx)("b",{children:r.mark.line}),", Col"," ",(0,n.jsx)("b",{children:r.mark.column}),", Pos"," ",(0,n.jsx)("b",{children:r.mark.position})]})]})]})})]})})}},12719:function(e,t,r){"use strict";r.d(t,{F:function(){return a},M:function(){return i}});var n=r(76649),s=r(65218);let i=r.n(s)()(()=>r.e(7088).then(r.bind(r,57088)).then(e=>e.default),{loadableGenerated:{webpack:()=>[57088]},ssr:!1}),a=e=>(0,n.Ln)({name:"string"},e)&&"YAMLException"===e.name},95327:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return R}});var n=r(24246),s=r(5152),i=r(27378),a=r(11596),l=r(43124),o=r(11032),c=r(37541),d=r(39514),u=r(34090),f=r(86677),h=r(45007),x=r(59389),g=r(9043),m=r(60136),p=r(77650),y=r(16781),j=r(36701),v=r(96878),b=r(10284),C=r(435);let w=e=>!("system_type"in e),A={url:"",classify:!1,classifyConfirmed:!1},k=x.Ry().shape({url:x.Z_().required().label("Database URL"),classify:x.O7(),classifyConfirmed:x.O7().when(["url","classify"],{is:(e,t)=>e&&t,then:()=>x.O7().equals([!0])})});var _=()=>{let[e,{isLoading:t}]=(0,C.pR)(),[r,{isLoading:i}]=(0,C.IR)(),[l,{isLoading:c}]=(0,v.Du)(),d=t||i||c,x=(0,s.pmc)(),_=(0,f.useRouter)(),z=(0,a.hz)(),S=(0,h.I0)(),L=async t=>{var r;let n=await e({organization_key:j.Av,generate:{config:{connection_string:t.url},target:b.GC.DB,type:b.j.DATASETS}});if("error"in n)return{error:(0,m.e$)(n.error)};let s=(null!==(r=n.data.generate_results)&&void 0!==r?r:[]).filter(w);return s&&s.length>0?{datasets:s}:{error:"Unable to generate a dataset with this connection."}},E=async e=>{let t=await r(e);return"error"in t?{error:(0,m.e$)(t.error)}:{dataset:t.data}},D=async e=>{let{values:t,datasets:r}=e,n=await l({dataset_schemas:r.map(e=>{let{name:t,fides_key:r}=e;return{fides_key:r,name:t}}),schema_config:{organization_key:j.Av,generate:{config:{connection_string:t.url},target:b.GC.DB,type:b.j.DATASETS}}});return"error"in n?{error:(0,m.e$)(n.error)}:{classifyInstances:n.data.classify_instances}},R=async e=>{var t;let r=await L(e);if("error"in r){x((0,y.Vo)(r.error));return}let n=await Promise.all(r.datasets.map(e=>E(e))),s=null!==(t=n.find(e=>"error"in e))&&void 0!==t?t:n[0];if("error"in s){x((0,y.Vo)(s.error));return}if(!e.classify){x((0,y.t5)("Generated ".concat(s.dataset.name," dataset"))),_.push({pathname:o.o5,query:{datasetId:s.dataset.fides_key}});return}let i=await D({values:e,datasets:r.datasets});if("error"in i){x((0,y.Vo)(i.error));return}x((0,y.t5)("Generate and classify are now in progress")),S((0,C.Zl)(s.dataset.fides_key)),_.push("/dataset")};return(0,n.jsx)(u.J9,{initialValues:{...A,classify:z.plus},validationSchema:k,onSubmit:R,validateOnChange:!1,validateOnBlur:!1,children:e=>{let{isSubmitting:t,errors:r,values:i,submitForm:a,resetForm:l,setFieldValue:o}=e;return(0,n.jsxs)(u.l0,{children:[(0,n.jsxs)(s.gCW,{spacing:8,align:"left",children:[(0,n.jsx)(s.xvT,{size:"sm",color:"gray.700",children:"Connect to a database using the connection URL. You may have received this URL from a colleague or your Ethyca developer support engineer."}),(0,n.jsx)(s.xuv,{children:(0,n.jsx)(g.j0,{name:"url",label:"Database URL"})}),z.plus?(0,n.jsx)(g.w8,{name:"classify",label:"Classify dataset",tooltip:"Use Fides Classify to suggest labels based on your data."}):null,(0,n.jsx)(s.xuv,{children:(0,n.jsx)(s.wpx,{type:"primary",htmlType:"submit",loading:t||d,disabled:t||d,"data-testid":"create-dataset-btn",children:"Generate dataset"})})]}),(0,n.jsx)(p.Z,{title:"Generate and classify this dataset",message:"You have chosen to generate and classify this dataset. This process may take several minutes. In the meantime you can continue using Fides. You will receive a notification when the process is complete.",isOpen:void 0!==r.classifyConfirmed,onClose:()=>{l({values:{...i,classifyConfirmed:!1}})},onConfirm:()=>{o("classifyConfirmed",!0),setTimeout(()=>{a()},0)}})]})}})},z=r(66527),S=r(53359),L=r(12719),E=r(50558),D=()=>{let[e]=(0,C.IR)(),[t,r]=(0,i.useState)(!0),[a,l]=(0,i.useState)(!1),[c,d]=(0,i.useState)(!1),u=(0,i.useRef)(null),h=(0,f.useRouter)(),x=(0,s.pmc)(),{errorAlert:g}=(0,S.V)(),[p,j]=(0,i.useState)(void 0),v=e=>{z.ZP.load(e,{json:!0}),j(void 0)},b=async t=>{let r;return"object"==typeof t&&null!=t&&"dataset"in t&&Array.isArray(t.dataset)?[r]=t.dataset:r=t,e(r)},w=e=>{x((0,y.t5)("Successfully loaded new dataset YAML")),(0,C.Zl)(e.fides_key),h.push({pathname:o.o5,query:{datasetId:e.fides_key}})},A=async()=>{l(!0);let e=u.current.getValue(),t=z.ZP.load(e,{json:!0}),r=await b(t);(0,m.D4)(r)?x((0,y.Vo)((0,m.e$)(r.error))):"data"in r&&w(r.data),l(!1)};return(0,n.jsxs)(s.kCb,{gap:"97px",children:[(0,n.jsxs)(s.xuv,{w:"75%",children:[(0,n.jsx)(s.xuv,{color:"gray.700",fontSize:"14px",mb:4,children:"Get started creating your first dataset by pasting your dataset yaml below! You may have received this yaml from a colleague or your Ethyca developer support engineer."}),(0,n.jsxs)(s.gCW,{align:"stretch",children:[(0,n.jsx)(s.izJ,{color:"gray.100"}),(0,n.jsx)(L.M,{defaultLanguage:"yaml",height:"calc(100vh - 515px)",onChange:e=>{try{d(!0),v(e),r(!!(!e||""===e.trim()))}catch(e){(0,L.F)(e)?j(e):g("Could not parse the supplied YAML")}},onMount:e=>{u.current=e,u.current.focus()},options:{fontFamily:"Menlo",fontSize:13,minimap:{enabled:!0}},theme:"light"}),(0,n.jsx)(s.izJ,{color:"gray.100"}),(0,n.jsx)(s.wpx,{type:"primary",disabled:t||!!p||a,loading:a,onClick:A,htmlType:"submit",className:"mt-6 w-fit",children:"Create dataset"})]})]}),(0,n.jsx)(s.xuv,{children:c&&(t||p)&&(0,n.jsx)(E.Z,{isEmptyState:t,yamlError:p})})]})},R=()=>{let e=(0,a.hz)(),[t,r]=(0,i.useState)(null);return(0,n.jsxs)(l.Z,{title:"Create New Dataset",mainProps:{paddingTop:0},children:[(0,n.jsx)(c.Z,{breadcrumbs:[{title:"Datasets",link:o.$m},{title:"Create new"}]}),(0,n.jsxs)(s.Kqy,{spacing:8,children:[(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.wpx,{onClick:()=>r("yaml"),"data-testid":"upload-yaml-btn",className:"mr-2",children:"Upload a Dataset YAML"}),(0,n.jsx)(s.wpx,{onClick:()=>r("database"),ghost:"database"===t,disabled:e.flags.dataDiscoveryAndDetection,className:"mr-2","data-testid":"connect-db-btn",children:"Connect to a database"}),e.flags.dataDiscoveryAndDetection?(0,n.jsx)(d.Z,{label:"Creating a dataset via a database connection is disabled when the 'detection & discovery' beta feature is enabled"}):null]}),"database"===t&&(0,n.jsx)(s.xuv,{w:{base:"100%",lg:"50%"},children:(0,n.jsx)(_,{})}),"yaml"===t&&(0,n.jsx)(s.xuv,{w:{base:"100%"},children:(0,n.jsx)(D,{})})]})]})}},41164:function(e,t,r){"use strict";r.d(t,{Bw:function(){return a},D4:function(){return s},Dy:function(){return o},XD:function(){return c},cz:function(){return d},hE:function(){return l},oK:function(){return i}});var n=r(76649);let s=e=>"error"in e,i=e=>(0,n.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,a=e=>(0,n.Ln)({status:"number",data:{}},e),l=e=>(0,n.Ln)({detail:"string"},e),o=e=>(0,n.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,n.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),d=e=>(0,n.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)},76649:function(e,t,r){"use strict";r.d(t,{Ln:function(){return n}});let n=(e,t)=>i(e,t),s=Symbol("SOME"),i=(e,t)=>"string"==typeof e?e===typeof t:Array.isArray(e)?s in e?e.some(e=>i(e,t)):!!Array.isArray(t)&&(0===e.length||t.every(t=>e.some(e=>i(e,t)))):"object"==typeof t&&null!==t&&Object.entries(e).every(([e,r])=>i(r,t[e]));class a{static narrow(e){return new a(t=>n(e,t))}constructor(e){this.NF=void 0,this.NF=e}satisfied(e){return this.NF(e)}build(e){return e}and(e){let t=this.NF,r=e instanceof a?e.NF:e instanceof Function?e:t=>n(e,t);return new a(e=>t(e)&&r(e))}}new a(e=>!0)}},function(e){e.O(0,[3005,2888,9774,179],function(){return e(e.s=73846)}),_N_E=e.O()}]);