"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7827],{79511:function(e,t,l){l.d(t,{k:function(){return r}});var i=l(76649);let n=e=>(0,i.Ln)({id:"string"},e),r=e=>(null!=e?e:[]).filter(n)},19535:function(e,t,l){l.d(t,{m:function(){return o}});var i=l(27378),n=l(11596),r=l(53359),s=l(96878),a=l(79511);let o=e=>{let{resourceFidesKey:t,resourceType:l}=e,{errorAlert:o}=(0,r.V)(),{plus:u}=(0,n.hz)(),d=(0,i.useMemo)(()=>null!=t?t:"",[]),c=(0,s.YU)(!0,{skip:!u}),p=(0,s.VN)(l,{skip:!u}),{data:x,isLoading:_,error:m,isError:f}=(0,s.PV)(null!=t?t:"",{skip:""!==d&&!(u&&d)}),[v]=(0,s._D)(),h=c.isLoading||p.isLoading||_,g=(0,i.useMemo)(()=>new Map((0,a.k)(c.data).map(e=>{var t;return[e.id,{...e,options:(null!==(t=e.allowed_values)&&void 0!==t?t:[]).map(e=>({value:e,label:e}))}]})),[c.data]),C=(0,i.useMemo)(()=>{var e;return null===(e=p.data)||void 0===e?void 0:e.filter(e=>e.active)},[p.data]),T=(0,i.useMemo)(()=>new Map((0,a.k)(C).map(e=>[e.id,e])),[C]),j=(0,i.useMemo)(()=>f&&(null==m?void 0:m.status)===404?new Map:new Map((0,a.k)(x).map(e=>[e.custom_field_definition_id,e])),[x,f,m]),A=(0,i.useMemo)(()=>{let e=[...T.keys()];return e.sort(),e},[T]),E=(0,i.useMemo)(()=>{let e={};return C&&j&&C.forEach(t=>{let l=j.get(t.id||"");l&&(t.allow_list_id&&"string[]"===t.field_type?e[l.custom_field_definition_id]=l.value:e[l.custom_field_definition_id]=l.value.toString())}),e},[C,j]),S=(0,i.useCallback)(async e=>{if(!u)return;let i="fides_key"in e&&""!==e.fides_key?e.fides_key:t;if(!i)return;let{customFieldValues:n}=e;if(!n||0===Object.keys(n).length)return;let r=[],s=[];A.forEach(e=>{let t=j.get(e),l=n[e];void 0===l||""===l||Array.isArray(l)&&0===l.length?(null==t?void 0:t.id)&&s.push(t.id):r.push({custom_field_definition_id:e,resource_id:i,id:null==t?void 0:t.id,value:l})});try{await v({resource_type:l,resource_id:i,upsert:r,delete:s})}catch(e){o("One or more custom fields have failed to save, please try again."),console.error(e)}},[u,j,o,t,A,v,l]);return{customFieldValues:E,definitionIdToCustomField:j,idToAllowListWithOptions:g,idToCustomFieldDefinition:T,isEnabled:u,isLoading:h,sortedCustomFieldDefinitionIds:A,upsertCustomFields:S}}},37827:function(e,t,l){l.d(t,{uc:function(){return f},Hn:function(){return o},Uv:function(){return s},C7:function(){return u},mZ:function(){return m.m}});var i,n,r,s,a=l(10284);(i=r||(r={}))[i.CREATE_CUSTOM_FIELDS=0]="CREATE_CUSTOM_FIELDS",i[i.CREATE_CUSTOM_LISTS=1]="CREATE_CUSTOM_LISTS",i[i.CHOOSE_FROM_LIBRARY=2]="CHOOSE_FROM_LIBRARY",a.AL.STRING,a.AL.STRING_,(n=s||(s={})).SINGLE_SELECT="singleSelect",n.MULTIPLE_SELECT="multipleSelect",n.OPEN_TEXT="openText";let o=[{label:"Single select",value:"singleSelect"},{label:"Multiple select",value:"multipleSelect"},{label:"Open Text",value:"openText"}],u=[{label:"taxonomy:".concat(a.P6.DATA_CATEGORY),value:a.P6.DATA_CATEGORY},{label:"taxonomy:".concat(a.P6.DATA_SUBJECT),value:a.P6.DATA_SUBJECT},{label:"taxonomy:".concat(a.P6.DATA_USE),value:a.P6.DATA_USE},{label:"".concat(a.P6.SYSTEM,":information"),value:a.P6.SYSTEM},{label:"system:data use",value:a.P6.PRIVACY_DECLARATION}];var d=l(24246),c=l(5152),p=l(34090),x=l(90982),_=l(9043),m=l(19535);let f=e=>{let{resourceFidesKey:t,resourceType:l}=e,{idToAllowListWithOptions:i,idToCustomFieldDefinition:n,isEnabled:r,isLoading:s,sortedCustomFieldDefinitionIds:o}=(0,m.m)({resourceFidesKey:t,resourceType:l});return r&&0!==o.length?(0,d.jsx)(x.Z,{heading:"Custom fields",children:(0,d.jsx)(c.kCb,{flexDir:"column","data-testid":"custom-fields-list",children:(0,d.jsx)(c.kCb,{flexDir:"column",gap:"24px",children:s?(0,d.jsx)(c.M5Y,{children:(0,d.jsx)(c.$jN,{})}):o.length>0&&(0,d.jsx)(c.kCb,{flexDirection:"column",gap:"12px",paddingBottom:"24px",children:o.map(e=>{let t=n.get(e);if(!t)return null;let l="customFieldValues.".concat(t.id);if(!t.allow_list_id&&t.field_type===a.AL.STRING)return(0,d.jsx)(p.gN,{name:l,children:e=>{let{field:l}=e;return(0,d.jsx)(_.j0,{...l,label:t.name,tooltip:t.description,variant:"stacked"})}},e);let r=i.get(t.allow_list_id);if(!r)return null;let{options:s}=r;return(0,d.jsx)(p.gN,{name:l,children:e=>{let{field:l}=e;return(0,d.jsx)(_.AP,{...l,isClearable:!0,isFormikOnChange:!0,isMulti:t.field_type!==a.AL.STRING,label:t.name,options:s,tooltip:t.description,variant:"stacked"})}},e)})})})})}):null};l(79511),l(27378)},53359:function(e,t,l){l.d(t,{H:function(){return r},V:function(){return i.V}});var i=l(75139),n=l(60136);let r=()=>{let{errorAlert:e}=(0,i.V)();return{handleError:t=>{let l="An unexpected error occurred. Please try again.";(0,n.Ot)(t)?l=t.data.detail:(0,n.tB)(t)&&(l=t.data.detail[0].msg),e(l)}}}},75139:function(e,t,l){l.d(t,{V:function(){return r}});var i=l(24246),n=l(5152);let r=()=>{let e=(0,n.pmc)();return{errorAlert:(t,l,r)=>{let s={...r,position:(null==r?void 0:r.position)||"top",render:e=>{let{onClose:r}=e;return(0,i.jsxs)(n.bZj,{alignItems:"normal",status:"error",children:[(0,i.jsx)(n.zMQ,{}),(0,i.jsxs)(n.xuv,{children:[l&&(0,i.jsx)(n.CdC,{children:l}),(0,i.jsx)(n.XaZ,{children:t})]}),(0,i.jsx)(n.PZ7,{onClick:r,position:"relative",right:0,size:"sm",top:-1})]})}};(null==r?void 0:r.id)&&e.isActive(r.id)?e.update(r.id,s):e(s)},successAlert:(t,l,r)=>{let s={...r,position:(null==r?void 0:r.position)||"top",render:e=>{let{onClose:r}=e;return(0,i.jsxs)(n.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,i.jsx)(n.zMQ,{}),(0,i.jsxs)(n.xuv,{children:[l&&(0,i.jsx)(n.CdC,{children:l}),(0,i.jsx)(n.XaZ,{children:t})]}),(0,i.jsx)(n.PZ7,{onClick:r,position:"relative",right:0,size:"sm",top:-1})]})}};(null==r?void 0:r.id)&&e.isActive(r.id)?e.update(r.id,s):e(s)}}}},90982:function(e,t,l){var i=l(24246),n=l(5152);t.Z=e=>{let{heading:t,HeadingButton:l,children:r}=e;return(0,i.jsx)(n.Kqy,{spacing:4,children:(0,i.jsxs)(n.xuv,{maxWidth:"720px",border:"1px",borderColor:"gray.200",borderRadius:6,overflow:"visible",mt:6,children:[(0,i.jsxs)(n.xuv,{backgroundColor:"gray.50",px:6,py:4,display:"flex",flexDirection:"row",alignItems:"center",borderBottom:"1px",borderColor:"gray.200",borderTopRadius:6,children:[(0,i.jsx)(n.X6q,{as:"h3",size:"xs",children:t}),l?(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(n.LZC,{}),(0,i.jsx)(l,{})]}):null]}),(0,i.jsx)(n.Kqy,{spacing:4,px:6,py:6,children:r})]})})}}}]);