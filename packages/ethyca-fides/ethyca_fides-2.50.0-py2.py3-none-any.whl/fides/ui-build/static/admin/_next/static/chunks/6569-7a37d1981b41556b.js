"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6569],{36848:function(e,s,t){t.d(s,{q:function(){return a}});var n=t(24246),i=t(5152);let a=e=>{let{label:s,isDisabled:t,...a}=e;return(0,n.jsx)(i.OK9,{"data-testid":"tab-".concat(s),_selected:{fontWeight:"600",color:"complimentary.500",borderColor:"complimentary.500"},fontSize:a.fontSize,fontWeight:"500",color:"gray.500",isDisabled:t||!1,children:s})};s.Z=e=>{let{data:s,border:t="partial",...l}=e;return(0,n.jsxs)(i.mQc,{colorScheme:"complimentary",...l,children:[(0,n.jsx)(i.tdY,{width:"partial"===t?"max-content":void 0,children:s.map(e=>(0,n.jsx)(a,{label:e.label,isDisabled:e.isDisabled,fontSize:l.fontSize},e.label))}),(0,n.jsx)(i.nPR,{children:s.map(e=>(0,n.jsx)(i.x45,{px:0,"data-testid":"tab-panel-".concat(e.label),children:e.content},e.label))})]})}},77650:function(e,s,t){var n=t(24246),i=t(5152);s.Z=e=>{let{isOpen:s,onClose:t,onConfirm:a,onCancel:l,title:r,message:d,cancelButtonText:o,continueButtonText:c,isLoading:x,returnFocusOnClose:h,isCentered:m,testId:u="confirmation-modal",icon:p}=e;return(0,n.jsxs)(i.u_l,{isOpen:s,onClose:t,size:"lg",returnFocusOnClose:null==h||h,isCentered:m,children:[(0,n.jsx)(i.ZAr,{}),(0,n.jsxs)(i.hzk,{textAlign:"center",p:6,"data-testid":u,children:[p?(0,n.jsx)(i.M5Y,{mb:2,children:p}):null,r?(0,n.jsx)(i.xBx,{fontWeight:"medium",pb:0,children:r}):null,d?(0,n.jsx)(i.fef,{children:d}):null,(0,n.jsx)(i.mzw,{children:(0,n.jsxs)(i.MIq,{columns:2,width:"100%",children:[(0,n.jsx)(i.wpx,{onClick:()=>{l&&l(),t()},size:"large",className:"mr-3","data-testid":"cancel-btn",disabled:x,children:o||"Cancel"}),(0,n.jsx)(i.wpx,{type:"primary",size:"large",onClick:a,"data-testid":"continue-btn",loading:x,children:c||"Continue"})]})})]})]})}},73485:function(e,s,t){t.d(s,{R:function(){return r}});var n=t(24246),i=t(5152),a=t(79894),l=t.n(a);let r=e=>{let{onClick:s,...t}=e;return(0,n.jsxs)(i.kCb,{alignItems:"center",mt:-4,mb:3,onClick:s,cursor:"pointer",...t,children:[(0,n.jsx)(i.wpx,{"aria-label":"Back",icon:(0,n.jsx)(i.Rpv,{}),className:"mr-2",size:"small"}),(0,n.jsx)(i.xvT,{as:"a",fontSize:"sm",fontWeight:"500",children:"Back"})]})};s.Z=e=>{let{backPath:s,...t}=e;return(0,n.jsxs)(i.kCb,{alignItems:"center",mb:6,...t,children:[(0,n.jsx)(i.wpx,{href:s,"aria-label":"Back",icon:(0,n.jsx)(i.Rpv,{}),className:"mr-2",size:"small"}),(0,n.jsx)(i.xvT,{as:l(),href:s,fontSize:"sm",fontWeight:"500",children:"Back"})]})}},91747:function(e,s,t){var n=t(24246),i=t(5152);t(27378);var a=t(43124),l=t(73485),r=t(11032);s.Z=e=>{let{children:s}=e;return(0,n.jsxs)(a.Z,{title:"User Management",children:[(0,n.jsx)(l.Z,{backPath:r.e3}),(0,n.jsx)(i.X6q,{fontSize:"2xl",fontWeight:"semibold",children:"User Management"}),s]})}},33990:function(e,s,t){t.d(s,{Z:function(){return H}});var n=t(24246),i=t(5152),a=t(49646),l=()=>(0,n.jsxs)(i.xuv,{children:[(0,n.jsx)(i.xuv,{pb:4,fontSize:"18px",fontWeight:"semibold",children:"Role Description"}),(0,n.jsx)(i.gCW,{spacing:4,children:a.K.map(e=>(0,n.jsxs)(i.xuv,{width:"100%",padding:4,borderRadius:"md",backgroundColor:"blue.50",fontSize:"14px",children:[(0,n.jsx)(i.xuv,{fontWeight:"semibold",children:e.label}),(0,n.jsx)(i.xuv,{color:"gray.500",children:e.description})]},e.roleKey))})]}),r=t(44296),d=t(36848),o=t(10284),c=t(38615),x=t(34090),h=t(86677),m=t(27378),u=t(60136),p=t(77650),j=t(11032),g=t(39514),f=t(16781),w=t(33312),b=t(22153),y=t(20133),v=t(31756);let C=e=>{let{assignedSystems:s,onAssignedSystemChange:t}=e,a=(0,r.C)(v.Ux);if((0,v.d6)(a,{skip:!a}),0===s.length)return null;let l=e=>{t(s.filter(s=>s.fides_key!==e.fides_key))};return(0,n.jsxs)(i.iA_,{size:"sm","data-testid":"assign-systems-delete-table",children:[(0,n.jsx)(i.hrZ,{children:(0,n.jsxs)(i.Tr,{children:[(0,n.jsx)(i.Th,{children:"System"}),(0,n.jsx)(i.Th,{})]})}),(0,n.jsx)(i.p3B,{children:s.map(e=>(0,n.jsxs)(i.Tr,{_hover:{bg:"gray.50"},"data-testid":"row-".concat(e.fides_key),children:[(0,n.jsx)(i.Td,{children:e.name}),(0,n.jsx)(i.Td,{textAlign:"end",children:(0,n.jsx)(i.wpx,{"aria-label":"Unassign system from user",icon:(0,n.jsx)(y.l,{}),onClick:()=>l(e),"data-testid":"unassign-btn"})})]},e.fides_key))})]})};var k=e=>{let{allSystems:s,assignedSystems:t,onChange:a}=e,l=e=>{t.find(s=>s.fides_key===e.fides_key)?a(t.filter(s=>s.fides_key!==e.fides_key)):a([...t,e])};return(0,n.jsx)(i.xuv,{overflowY:"auto",maxHeight:"300px",children:(0,n.jsxs)(i.iA_,{size:"sm","data-testid":"assign-systems-table",maxHeight:"50vh",overflowY:"scroll",children:[(0,n.jsx)(i.hrZ,{position:"sticky",top:0,background:"white",zIndex:1,children:(0,n.jsxs)(i.Tr,{children:[(0,n.jsx)(i.Th,{children:"System"}),(0,n.jsx)(i.Th,{children:"Assign"})]})}),(0,n.jsx)(i.p3B,{children:s.map(e=>{let s=!!t.find(s=>s.fides_key===e.fides_key);return(0,n.jsxs)(i.Tr,{_hover:{bg:"gray.50"},"data-testid":"row-".concat(e.fides_key),children:[(0,n.jsx)(i.Td,{children:e.name}),(0,n.jsx)(i.Td,{children:(0,n.jsx)(i.rAg,{checked:s,onChange:()=>l(e),"data-testid":"assign-switch"})})]},e.fides_key)})})]})})};let S=(e,s)=>{var t,n;return(null===(t=e.name)||void 0===t?void 0:t.toLocaleLowerCase().includes(s.toLocaleLowerCase()))||(null===(n=e.description)||void 0===n?void 0:n.toLocaleLowerCase().includes(s.toLocaleLowerCase()))};var _=e=>{let{isOpen:s,onClose:t,assignedSystems:a,onAssignedSystemChange:l}=e,{data:r}=(0,b.K3)(),[d,o]=(0,m.useState)(""),[c,x]=(0,m.useState)(a),h=async()=>{l(c),t()},u=!r||0===r.length,p=(0,m.useMemo)(()=>r?r.filter(e=>S(e,d)):[],[r,d]),j=(0,m.useMemo)(()=>{let e=new Set(c.map(e=>e.fides_key));return p.every(s=>e.has(s.fides_key))},[p,c]);return(0,n.jsxs)(i.u_l,{isOpen:s,onClose:t,size:"2xl",children:[(0,n.jsx)(i.ZAr,{}),(0,n.jsxs)(i.hzk,{p:8,"data-testid":"confirmation-modal",children:[(0,n.jsxs)(i.xBx,{fontWeight:"medium",display:"flex",justifyContent:"space-between",alignItems:"center",children:[(0,n.jsx)(i.xvT,{children:"Assign systems"}),(0,n.jsxs)(i.Cts,{bg:"green.500",color:"white",px:1,children:["Assigned to ",a.length," systems"]})]}),(0,n.jsx)(i.fef,{"data-testid":"assign-systems-modal-body",children:u?(0,n.jsx)(i.xvT,{children:"No systems found"}):(0,n.jsxs)(i.Kqy,{spacing:4,children:[(0,n.jsxs)(i.kCb,{justifyContent:"space-between",children:[(0,n.jsx)(i.xvT,{fontSize:"sm",flexGrow:1,fontWeight:"medium",children:"Assign systems in your organization to this user"}),(0,n.jsx)(i.xuv,{children:(0,n.jsxs)(i.NIc,{display:"flex",alignItems:"center",children:[(0,n.jsx)(i.lXp,{fontSize:"sm",htmlFor:"assign-all-systems",mb:"0",children:"Assign all systems"}),(0,n.jsx)(i.rAg,{size:"small",id:"assign-all-systems",checked:j,onChange:e=>{e&&r?x(p):x(r?r.filter(e=>!p.includes(e)):[])},"data-testid":"assign-all-systems-toggle"})]})})]}),(0,n.jsx)(w.Z,{search:d,onChange:o,placeholder:"Search for systems","data-testid":"system-search",withIcon:!0}),(0,n.jsx)(k,{allSystems:p,assignedSystems:c,onChange:x})]})}),(0,n.jsx)(i.mzw,{justifyContent:"flex-start",children:(0,n.jsxs)("div",{children:[(0,n.jsx)(i.wpx,{onClick:t,className:"mr-2","data-testid":"cancel-btn",children:"Cancel"}),u?null:(0,n.jsx)(i.wpx,{type:"primary",onClick:h,"data-testid":"confirm-btn",children:"Confirm"})]})})]})]})},P=e=>{let{label:s,roleKey:t,isSelected:a,isDisabled:l,assignedSystems:r,onAssignedSystemChange:d}=e,{setFieldValue:c}=(0,x.u6)(),h=(0,i.qY0)(),m=l?"You do not have sufficient permissions to assign this role.":void 0;return a?(0,n.jsxs)(i.Kqy,{borderRadius:"md",border:"1px solid",borderColor:"gray.200",p:4,backgroundColor:"gray.50","aria-selected":"true",spacing:4,"data-testid":"selected",children:[(0,n.jsxs)(i.kCb,{alignItems:"center",justifyContent:"space-between",children:[(0,n.jsx)(i.xvT,{fontSize:"md",fontWeight:"semibold",children:s}),(0,n.jsx)(i.StI,{})]}),t!==o.A7.APPROVER?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(i.kCb,{alignItems:"center",children:[(0,n.jsx)(i.xvT,{fontSize:"sm",fontWeight:"semibold",mr:1,children:"Assigned systems"}),(0,n.jsx)(g.Z,{label:"Assigned systems refer to those systems that have been specifically allocated to a user for management purposes. Users assigned to a system possess full edit permissions and are listed as the Data Steward for the respective system."})]}),(0,n.jsx)(i.wpx,{disabled:l,title:m,type:"primary",size:"small",onClick:h.onOpen,"data-testid":"assign-systems-btn",children:"Assign systems +"}),(0,n.jsx)(C,{assignedSystems:r,onAssignedSystemChange:d}),h.isOpen?(0,n.jsx)(_,{isOpen:h.isOpen,onClose:h.onClose,assignedSystems:r,onAssignedSystemChange:d}):null]}):null]}):(0,n.jsx)(i.wpx,{onClick:()=>{c("roles",[t])},"data-testid":"role-option-".concat(s),title:m,disabled:l,children:s})};let R={roles:[]};var z=()=>{var e;let s=(0,i.pmc)(),t=(0,h.useRouter)(),l=(0,r.C)(v.Ux);(0,v.d6)(l,{skip:!l});let{isOpen:d,onOpen:w,onClose:b}=(0,i.qY0)(),y=(0,r.C)(v.R$),[C,k]=(0,m.useState)(y),[S]=(0,v.G$)();(0,m.useEffect)(()=>{k(y)},[y]);let{data:_,isLoading:z}=(0,v.gU)(null!=l?l:"",{skip:!l}),[T]=(0,v.lD)(),A=async e=>{if(d&&b(),!l)return;let t=e.roles.includes(o.A7.APPROVER),n=await T({user_id:l,payload:{roles:e.roles}});if((0,u.D4)(n)){s((0,f.Vo)((0,u.e$)(n.error)));return}if(!t){let e=C.map(e=>e.fides_key),t=await S({userId:l,fidesKeys:e});if((0,u.D4)(t)){s((0,f.Vo)((0,u.e$)(t.error)));return}}s((0,f.t5)("Permissions updated"))},I=async e=>{l&&(C.length>0&&e.roles.includes(o.A7.APPROVER)?w():await A(e))},q=(0,c.Tg)([o.Sh.USER_PERMISSION_ASSIGN_OWNERS]);if(!l)return null;if(z)return(0,n.jsx)(i.$jN,{});if(!q&&(null==_?void 0:null===(e=_.roles)||void 0===e?void 0:e.includes(o.A7.OWNER)))return(0,n.jsx)(i.xvT,{"data-testid":"insufficient-access",children:"You do not have sufficient access to change this user's permissions."});let E=(null==_?void 0:_.roles)?{roles:_.roles}:R;return(0,n.jsx)(x.J9,{onSubmit:I,initialValues:E,enableReinitialize:!0,children:e=>{let{values:s,isSubmitting:l,dirty:r}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsxs)(i.Kqy,{spacing:7,children:[(0,n.jsxs)(i.Kqy,{spacing:3,"data-testid":"role-options",children:[(0,n.jsxs)(i.kCb,{alignItems:"center",children:[(0,n.jsx)(i.xvT,{fontSize:"sm",fontWeight:"semibold",mr:1,children:"User role"}),(0,n.jsx)(g.Z,{label:"A user's role in the organization determines what parts of the UI they can access and which functions are available to them."})]}),a.K.map(e=>{let t=s.roles.indexOf(e.roleKey)>=0;return(0,n.jsx)(P,{isSelected:t,isDisabled:e.roleKey===o.A7.OWNER&&!q,assignedSystems:C,onAssignedSystemChange:k,...e},e.roleKey)})]}),(0,n.jsxs)("div",{children:[(0,n.jsx)(i.wpx,{onClick:()=>t.push(j.e3),children:"Cancel"}),(0,n.jsx)(i.wpx,{type:"primary",htmlType:"submit",loading:l,disabled:!r&&C===y,"data-testid":"save-btn",children:"Save"})]})]}),(0,n.jsx)(p.Z,{isOpen:d,onClose:b,onConfirm:()=>A(s),title:"Change role to Approver",testId:"downgrade-to-approver-confirmation-modal",continueButtonText:"Yes",message:(0,n.jsx)(i.xvT,{children:"Switching to an approver role will remove all assigned systems. Do you wish to proceed?"})})]})}})},T=t(72763),A=t(59389),I=t(11596),q=t(9043),E=t(42252);let{useGetEmailInviteStatusQuery:N}=t(21618).u.injectEndpoints({endpoints:e=>({getEmailInviteStatus:e.query({query:()=>({url:"/messaging/email-invite/status"}),providesTags:()=>["Email Invite Status"]})})});var O=t(91664),Z=t(36223),U=t(43073);let W=A.Ry().shape({password:E.a.label("Password"),passwordConfirmation:A.Z_().required().oneOf([A.iH("password")],"Passwords must match").label("Password confirmation")}),D={password:"",passwordConfirmation:""},B=e=>{let s=(0,i.qY0)(),t=(0,i.pmc)(),[n]=(0,v.ls)(),a=async i=>{let a=await n({id:e,new_password:i.password});(0,U.D4)(a)?t((0,f.Vo)((0,u.e$)(a.error))):(t((0,f.t5)("Successfully reset user's password. Please inform the user of their new password.")),s.onClose())};return{...s,handleResetPassword:a}};var K=e=>{let{id:s}=e,{handleResetPassword:t,isOpen:a,onClose:l,onOpen:r}=B(s);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(i.wpx,{onClick:r,"data-testid":"reset-password-btn",children:"Reset password"}),(0,n.jsxs)(i.u_l,{isCentered:!0,isOpen:a,onClose:l,children:[(0,n.jsx)(i.ZAr,{}),(0,n.jsx)(i.hzk,{children:(0,n.jsx)(x.J9,{initialValues:D,validationSchema:W,onSubmit:t,children:e=>{let{isSubmitting:s,dirty:t,isValid:a}=e;return(0,n.jsxs)(x.l0,{children:[(0,n.jsx)(i.xBx,{children:"Reset Password"}),(0,n.jsx)(i.olH,{}),(0,n.jsx)(i.fef,{children:(0,n.jsxs)(i.Kqy,{direction:"column",spacing:4,children:[(0,n.jsx)(i.xvT,{mb:2,children:"Choose a new password for this user."}),(0,n.jsx)(q.j0,{name:"password",label:"Password",placeholder:"********",type:"password",tooltip:"Password must contain at least 8 characters, 1 number, 1 capital letter, 1 lowercase letter, and at least 1 symbol.",autoComplete:"new-password"}),(0,n.jsx)(q.j0,{name:"passwordConfirmation",label:"Confirm Password",placeholder:"********",type:"password",tooltip:"Must match above password.",autoComplete:"confirm-password"})]})}),(0,n.jsx)(i.mzw,{children:(0,n.jsxs)("div",{className:"w-full gap-2",children:[(0,n.jsx)(i.wpx,{onClick:l,className:"w-1/2",children:"Cancel"}),(0,n.jsx)(i.wpx,{type:"primary",disabled:!t||!a,loading:s,htmlType:"submit",className:"w-1/2","data-testid":"submit-btn",children:"Change Password"})]})})]})}})})]})]})};let L=e=>{let s=(0,i.qY0)(),t=(0,i.pmc)(),[n,a]=(0,m.useState)(""),[l,r]=(0,m.useState)(""),[d,{isLoading:o}]=(0,v.ev)(),c=!!(e&&l&&n),x=async()=>{c&&d({id:e,old_password:n,new_password:l}).unwrap().then(()=>{t((0,f.t5)("Password updated")),s.onClose()})};return{...s,changePasswordValidation:c,handleChange:e=>{"oldPassword"===e.target.name?a(e.target.value):r(e.target.value)},handleChangePassword:x,isLoading:o,newPasswordValue:l,oldPasswordValue:n}};var V=e=>{let{id:s}=e,{changePasswordValidation:t,handleChange:a,handleChangePassword:l,isLoading:r,isOpen:d,newPasswordValue:o,oldPasswordValue:c,onClose:x,onOpen:h}=L(s);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(i.wpx,{onClick:h,"data-testid":"update-password-btn",children:"Update password"}),(0,n.jsxs)(i.u_l,{isCentered:!0,isOpen:d,onClose:x,children:[(0,n.jsx)(i.ZAr,{}),(0,n.jsxs)(i.hzk,{children:[(0,n.jsx)(i.xBx,{children:"Update Password"}),(0,n.jsx)(i.olH,{}),(0,n.jsx)(i.fef,{pb:6,children:(0,n.jsxs)(i.Kqy,{direction:"column",spacing:"15px",children:[(0,n.jsx)(i.NIc,{children:(0,n.jsx)(i.IIB,{isRequired:!0,name:"oldPassword",onChange:a,placeholder:"Old Password",type:"password",value:c,"data-testid":"input-oldPassword"})}),(0,n.jsx)(i.NIc,{children:(0,n.jsx)(i.IIB,{isRequired:!0,name:"newPassword",onChange:a,placeholder:"New Password",type:"password",value:o,"data-testid":"input-newPassword"})})]})}),(0,n.jsxs)(i.mzw,{children:[(0,n.jsx)(i.wpx,{onClick:x,className:"mr-2 w-1/2",children:"Cancel"}),(0,n.jsx)(i.wpx,{type:"primary",disabled:!t,loading:r,onClick:l,htmlType:"submit",className:"mr-3 w-1/2","data-testid":"submit-btn",children:"Change Password"})]})]})]})]})},Y=()=>{let e=(0,r.C)(v.Ux),s=(0,r.C)(Z.dy),t=!!s&&s.id===e;return(0,n.jsx)(i.xuv,{children:e?(0,n.jsxs)(i.Ugi,{children:[t?(0,n.jsx)(V,{id:e}):null,(0,n.jsx)(c.ZP,{scopes:[o.Sh.USER_PASSWORD_RESET],children:(0,n.jsx)(K,{id:e})})]}):null})};let M={username:"",first_name:"",email_address:"",last_name:"",password:""},F=A.Ry().shape({username:A.Z_().required().label("Username"),email_address:A.Z_().email().required().label("Email address"),first_name:A.Z_().label("First name"),last_name:A.Z_().label("Last name"),password:E.a.label("Password")});var $=e=>{let{onSubmit:s,initialValues:t,canEditNames:a}=e,l=(0,h.useRouter)(),d=(0,i.pmc)(),o=(0,r.T)(),c=(0,i.qY0)(),m=(0,r.C)(v.ZC),{data:p}=N(),g=null==p?void 0:p.enabled,{flags:w}=(0,I.Vb)(),b=!m,C=!b&&!a,k=b&&!g,S=async e=>{let{password:t,...n}=e,i=await s(k?e:n);if((0,u.D4)(i)){d((0,f.Vo)((0,u.e$)(i.error)));return}d((0,f.t5)("".concat(b?"User created. By default, new users are set to the Viewer role. To change the role, please go to the Permissions tab.":"User updated."))),(null==i?void 0:i.data)&&o((0,v.Vv)(i.data.id))},_=F,{data:P}=(0,O.qv)(),R=!w.ssoAuthentication||!(null==P?void 0:P.length);return R||(_=F.shape({password:E.a.optional().label("Password")})),_=k?_:_.omit(["password"]),(0,n.jsx)(x.J9,{onSubmit:S,initialValues:null!=t?t:M,validationSchema:_,children:e=>{let{dirty:s,isSubmitting:t,isValid:a}=e;return(0,n.jsx)(x.l0,{children:(0,n.jsxs)(i.Kqy,{maxW:["xs","xs","100%"],width:"100%",spacing:7,children:[(0,n.jsxs)(i.Kqy,{spacing:6,maxWidth:"55%",children:[(0,n.jsxs)(i.kCb,{children:[(0,n.jsxs)(i.xvT,{display:"flex",alignItems:"center",fontSize:"sm",fontWeight:"semibold",children:["Profile"," ",(null==m?void 0:m.disabled)&&(0,n.jsx)(i.Cts,{bg:"green.500",color:"white",paddingLeft:"2",marginLeft:"2",textTransform:"none",paddingRight:"8px",height:"18px",lineHeight:"18px",borderRadius:"6px",fontWeight:"500",textAlign:"center","data-testid":"invite-sent-badge",children:"Invite sent"})]}),(0,n.jsx)(i.xuv,{marginLeft:"auto",children:(0,n.jsxs)(i.Ugi,{children:[(0,n.jsx)(Y,{}),b?null:(0,n.jsxs)(i.xuv,{children:[(0,n.jsx)(i.wpx,{"aria-label":"delete",icon:(0,n.jsx)(y.l,{}),onClick:c.onOpen,"data-testid":"delete-user-btn"}),(0,n.jsx)(T.Z,{user:m,...c})]})]})})]}),(0,n.jsx)(q.j0,{name:"username",label:"Username",variant:"block",placeholder:"Enter new username",disabled:!b,isRequired:!0}),(0,n.jsx)(q.j0,{name:"email_address",label:"Email address",variant:"block",placeholder:"Enter email of user",isRequired:!0}),(0,n.jsx)(q.j0,{name:"first_name",label:"First Name",variant:"block",placeholder:"Enter first name of user",disabled:C}),(0,n.jsx)(q.j0,{name:"last_name",label:"Last Name",variant:"block",placeholder:"Enter last name of user",disabled:C}),k?(0,n.jsx)(q.j0,{name:"password",label:"Password",variant:"block",placeholder:"********",type:"password",tooltip:"Password must contain at least 8 characters, 1 number, 1 capital letter, 1 lowercase letter, and at least 1 symbol.",isRequired:R}):null]}),(0,n.jsxs)("div",{children:[(0,n.jsx)(i.wpx,{onClick:()=>l.push(j.e3),className:"mr-3",children:"Cancel"}),(0,n.jsx)(i.wpx,{htmlType:"submit",type:"primary",disabled:!s||!a,loading:t,"data-testid":"save-user-btn",children:"Save"})]})]})})}})},H=e=>{let{onSubmit:s,initialValues:t,...a}=e,x=(0,r.C)(v.Ux);(0,v.Fk)(x,{skip:!x});let h=(0,c.Tg)([o.Sh.USER_PERMISSION_UPDATE]),m=[{label:"Profile",content:(0,n.jsx)($,{onSubmit:s,initialValues:t,...a})},{label:"Permissions",content:(0,n.jsxs)(i.kCb,{gap:"97px",children:[(0,n.jsx)(i.xuv,{w:{base:"100%",md:"50%",xl:"50%"},children:(0,n.jsx)(z,{})}),(0,n.jsx)(i.xuv,{position:"absolute",top:"96px",right:6,height:"calc(100% + 100px)",overflowY:"scroll",padding:6,w:"35%",borderLeftWidth:"1px",children:(0,n.jsx)(l,{})})]}),isDisabled:!x||!h}];return(0,n.jsx)(d.Z,{data:m})}},43073:function(e,s,t){t.d(s,{Bw:function(){return n.Bw},D4:function(){return n.D4}});var n=t(41164)}}]);