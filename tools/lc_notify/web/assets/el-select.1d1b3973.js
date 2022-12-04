import{bg as yl,bh as Ll,b4 as El,a1 as Le,j as c,bi as Ee,bj as D,a2 as q,t as oe,at as ol,c as Me,h as ae,au as $e,b6 as tl,b9 as Ml,Q as E,_ as Ve,ad as me,ao as il,n as b,y as $,D as ie,q as P,H as J,s as h,M as U,r as A,m as al,bb as Cl,v as te,$ as sl,bk as cl,a0 as $l,a7 as Vl,a4 as pl,a3 as Pl,ac as ne,bl as fe,bm as kl,bn as ll,l as fl,a as vl,U as Y,i as zl,ab as Bl,bo as Dl,C as Sl,J as ql,az as Fl,E as Wl,P as Kl,z as Al,an as Rl,u as Hl,av as ml,Y as Nl,af as jl,bp as Ql,bq as Gl,a8 as Ol,br as _,bs as Ul,x as ve,w as L,p as K,F as nl,B as bl,aa as z,ah as Jl,L as B,bt as Yl,O as Xl,a9 as hl,T as Zl,aI as wl}from"./index.3384dca8.js";import{u as xl}from"./el-form-item.6d54d76a.js";const _l=(e="")=>e.replace(/[|\\{}()[\]^$+*?.]/g,"\\$&").replace(/-/g,"\\x2d");function en(e,l){if(!yl)return;if(!l){e.scrollTop=0;return}const i=[];let p=l.offsetParent;for(;p!==null&&e!==p&&e.contains(p);)i.push(p),p=p.offsetParent;const m=l.offsetTop+i.reduce((y,C)=>y+C.offsetTop,0),d=m+l.offsetHeight,s=e.scrollTop,u=s+e.clientHeight;m<s?e.scrollTop=m:d>u&&(e.scrollTop=d-e.clientHeight)}const ln=e=>Ll[e||"default"],nn=e=>["",...El].includes(e),on=e=>({focus:()=>{var l,i;(i=(l=e.value)==null?void 0:l.focus)==null||i.call(l)}}),Tl="ElSelectGroup",Pe="ElSelect";function tn(e,l){const i=Le(Pe),p=Le(Tl,{disabled:!1}),m=c(()=>Object.prototype.toString.call(e.value).toLowerCase()==="[object object]"),d=c(()=>i.props.multiple?w(i.props.modelValue,e.value):T(e.value,i.props.modelValue)),s=c(()=>{if(i.props.multiple){const f=i.props.modelValue||[];return!d.value&&f.length>=i.props.multipleLimit&&i.props.multipleLimit>0}else return!1}),u=c(()=>e.label||(m.value?"":e.value)),y=c(()=>e.value||e.label||""),C=c(()=>e.disabled||l.groupDisabled||s.value),v=ol(),w=(f=[],g)=>{if(m.value){const S=i.props.valueKey;return f&&f.some(F=>Ee(D(F,S))===D(g,S))}else return f&&f.includes(g)},T=(f,g)=>{if(m.value){const{valueKey:S}=i.props;return D(f,S)===D(g,S)}else return f===g},M=()=>{!e.disabled&&!p.disabled&&(i.hoverIndex=i.optionsArray.indexOf(v.proxy))};q(()=>u.value,()=>{!e.created&&!i.props.remote&&i.setSelected()}),q(()=>e.value,(f,g)=>{const{remote:S,valueKey:F}=i.props;if(Object.is(f,g)||(i.onOptionDestroy(g,v.proxy),i.onOptionCreate(v.proxy)),!e.created&&!S){if(F&&typeof f=="object"&&typeof g=="object"&&f[F]===g[F])return;i.setSelected()}}),q(()=>p.disabled,()=>{l.groupDisabled=p.disabled},{immediate:!0});const{queryChange:t}=Ee(i);return q(t,f=>{const{query:g}=oe(f),S=new RegExp(_l(g),"i");l.visible=S.test(u.value)||e.created,l.visible||i.filteredOptionsCount--}),{select:i,currentLabel:u,currentValue:y,itemSelected:d,isDisabled:C,hoverItem:M}}const an=Me({name:"ElOption",componentName:"ElOption",props:{value:{required:!0,type:[String,Number,Boolean,Object]},label:[String,Number],created:Boolean,disabled:{type:Boolean,default:!1}},setup(e){const l=ae("select"),i=$e({index:-1,groupDisabled:!1,visible:!0,hitState:!1,hover:!1}),{currentLabel:p,itemSelected:m,isDisabled:d,select:s,hoverItem:u}=tn(e,i),{visible:y,hover:C}=tl(i),v=ol().proxy;s.onOptionCreate(v),Ml(()=>{const T=v.value,{selected:M}=s,f=(s.props.multiple?M:[M]).some(g=>g.value===v.value);E(()=>{s.cachedOptions.get(T)===v&&!f&&s.cachedOptions.delete(T)}),s.onOptionDestroy(T,v)});function w(){e.disabled!==!0&&i.groupDisabled!==!0&&s.handleOptionSelect(v,!0)}return{ns:l,currentLabel:p,itemSelected:m,isDisabled:d,select:s,hoverItem:u,visible:y,hover:C,selectOptionClick:w,states:i}}});function sn(e,l,i,p,m,d){return me((b(),$("li",{class:h([e.ns.be("dropdown","item"),e.ns.is("disabled",e.isDisabled),{selected:e.itemSelected,hover:e.hover}]),onMouseenter:l[0]||(l[0]=(...s)=>e.hoverItem&&e.hoverItem(...s)),onClick:l[1]||(l[1]=U((...s)=>e.selectOptionClick&&e.selectOptionClick(...s),["stop"]))},[ie(e.$slots,"default",{},()=>[P("span",null,J(e.currentLabel),1)])],34)),[[il,e.visible]])}var rl=Ve(an,[["render",sn],["__file","/home/runner/work/element-plus/element-plus/packages/components/select/src/option.vue"]]);const rn=Me({name:"ElSelectDropdown",componentName:"ElSelectDropdown",setup(){const e=Le(Pe),l=ae("select"),i=c(()=>e.props.popperClass),p=c(()=>e.props.multiple),m=c(()=>e.props.fitInputWidth),d=A("");function s(){var u;d.value=`${(u=e.selectWrapper)==null?void 0:u.offsetWidth}px`}return al(()=>{s(),Cl(e.selectWrapper,s)}),{ns:l,minWidth:d,popperClass:i,isMultiple:p,isFitInputWidth:m}}});function un(e,l,i,p,m,d){return b(),$("div",{class:h([e.ns.b("dropdown"),e.ns.is("multiple",e.isMultiple),e.popperClass]),style:te({[e.isFitInputWidth?"width":"minWidth"]:e.minWidth})},[ie(e.$slots,"default")],6)}var dn=Ve(rn,[["render",un],["__file","/home/runner/work/element-plus/element-plus/packages/components/select/src/select-dropdown.vue"]]);function cn(e){const{t:l}=sl();return $e({options:new Map,cachedOptions:new Map,createdLabel:null,createdSelected:!1,selected:e.multiple?[]:{},inputLength:20,inputWidth:0,optionsCount:0,filteredOptionsCount:0,visible:!1,softFocus:!1,selectedLabel:"",hoverIndex:-1,query:"",previousQuery:null,inputHovering:!1,cachedPlaceHolder:"",currentPlaceholder:l("el.select.placeholder"),menuVisibleOnFocus:!1,isOnComposition:!1,isSilentBlur:!1,prefixWidth:11,tagInMultiLine:!1,mouseEnter:!1})}const pn=(e,l,i)=>{const{t:p}=sl(),m=ae("select");xl({from:"suffixTransition",replacement:"override style scheme",version:"2.3.0",scope:"props",ref:"https://element-plus.org/en-US/component/select.html#select-attributes"},c(()=>e.suffixTransition===!1));const d=A(null),s=A(null),u=A(null),y=A(null),C=A(null),v=A(null),w=A(-1),T=cl({query:""}),M=cl(""),{form:t,formItem:f}=$l(),g=c(()=>!e.filterable||e.multiple||!l.visible),S=c(()=>e.disabled||(t==null?void 0:t.disabled)),F=c(()=>{const n=e.multiple?Array.isArray(e.modelValue)&&e.modelValue.length>0:e.modelValue!==void 0&&e.modelValue!==null&&e.modelValue!=="";return e.clearable&&!S.value&&l.inputHovering&&n}),se=c(()=>e.remote&&e.filterable&&!e.remoteShowSuffix?"":e.suffixIcon),ke=c(()=>m.is("reverse",se.value&&l.visible&&e.suffixTransition)),be=c(()=>e.remote?300:0),re=c(()=>e.loading?e.loadingText||p("el.select.loading"):e.remote&&l.query===""&&l.options.size===0?!1:e.filterable&&l.query&&l.options.size>0&&l.filteredOptionsCount===0?e.noMatchText||p("el.select.noMatch"):l.options.size===0?e.noDataText||p("el.select.noData"):null),I=c(()=>Array.from(l.options.values())),ze=c(()=>Array.from(l.cachedOptions.values())),Be=c(()=>{const n=I.value.filter(o=>!o.created).some(o=>o.currentLabel===l.query);return e.filterable&&e.allowCreate&&l.query!==""&&!n}),ee=Vl(),De=c(()=>["small"].includes(ee.value)?"small":"default"),qe=c({get(){return l.visible&&re.value!==!1},set(n){l.visible=n}});q([()=>S.value,()=>ee.value,()=>t==null?void 0:t.size],()=>{E(()=>{W()})}),q(()=>e.placeholder,n=>{l.cachedPlaceHolder=l.currentPlaceholder=n}),q(()=>e.modelValue,(n,o)=>{e.multiple&&(W(),n&&n.length>0||s.value&&l.query!==""?l.currentPlaceholder="":l.currentPlaceholder=l.cachedPlaceHolder,e.filterable&&!e.reserveKeyword&&(l.query="",H(l.query))),ue(),e.filterable&&!e.multiple&&(l.inputLength=20),!pl(n,o)&&e.validateEvent&&(f==null||f.validate("change").catch(a=>Pl()))},{flush:"post",deep:!0}),q(()=>l.visible,n=>{var o,a,r;n?((a=(o=u.value)==null?void 0:o.updatePopper)==null||a.call(o),e.filterable&&(l.filteredOptionsCount=l.optionsCount,l.query=e.remote?"":l.selectedLabel,e.multiple?(r=s.value)==null||r.focus():l.selectedLabel&&(l.currentPlaceholder=`${l.selectedLabel}`,l.selectedLabel=""),H(l.query),!e.multiple&&!e.remote&&(T.value.query="",fe(T),fe(M)))):(e.filterable&&(ne(e.filterMethod)&&e.filterMethod(""),ne(e.remoteMethod)&&e.remoteMethod("")),s.value&&s.value.blur(),l.query="",l.previousQuery=null,l.selectedLabel="",l.inputLength=20,l.menuVisibleOnFocus=!1,Fe(),E(()=>{s.value&&s.value.value===""&&l.selected.length===0&&(l.currentPlaceholder=l.cachedPlaceHolder)}),e.multiple||(l.selected&&(e.filterable&&e.allowCreate&&l.createdSelected&&l.createdLabel?l.selectedLabel=l.createdLabel:l.selectedLabel=l.selected.currentLabel,e.filterable&&(l.query=l.selectedLabel)),e.filterable&&(l.currentPlaceholder=l.cachedPlaceHolder))),i.emit("visible-change",n)}),q(()=>l.options.entries(),()=>{var n,o,a;if(!yl)return;(o=(n=u.value)==null?void 0:n.updatePopper)==null||o.call(n),e.multiple&&W();const r=((a=C.value)==null?void 0:a.querySelectorAll("input"))||[];Array.from(r).includes(document.activeElement)||ue(),e.defaultFirstOption&&(e.filterable||e.remote)&&l.filteredOptionsCount&&ge()},{flush:"post"}),q(()=>l.hoverIndex,n=>{kl(n)&&n>-1?w.value=I.value[n]||{}:w.value={},I.value.forEach(o=>{o.hover=w.value===o})});const W=()=>{e.collapseTags&&!e.filterable||E(()=>{var n,o;if(!d.value)return;const a=d.value.$el.querySelector("input"),r=y.value,O=ln(ee.value||(t==null?void 0:t.size));a.style.height=`${(l.selected.length===0?O:Math.max(r?r.clientHeight+(r.clientHeight>O?6:0):0,O))-2}px`,l.tagInMultiLine=Number.parseFloat(a.style.height)>=O,l.visible&&re.value!==!1&&((o=(n=u.value)==null?void 0:n.updatePopper)==null||o.call(n))})},H=async n=>{if(!(l.previousQuery===n||l.isOnComposition)){if(l.previousQuery===null&&(ne(e.filterMethod)||ne(e.remoteMethod))){l.previousQuery=n;return}l.previousQuery=n,E(()=>{var o,a;l.visible&&((a=(o=u.value)==null?void 0:o.updatePopper)==null||a.call(o))}),l.hoverIndex=-1,e.multiple&&e.filterable&&E(()=>{const o=s.value.value.length*15+20;l.inputLength=e.collapseTags?Math.min(50,o):o,he(),W()}),e.remote&&ne(e.remoteMethod)?(l.hoverIndex=-1,e.remoteMethod(n)):ne(e.filterMethod)?(e.filterMethod(n),fe(M)):(l.filteredOptionsCount=l.optionsCount,T.value.query=n,fe(T),fe(M)),e.defaultFirstOption&&(e.filterable||e.remote)&&l.filteredOptionsCount&&(await E(),ge())}},he=()=>{l.currentPlaceholder!==""&&(l.currentPlaceholder=s.value.value?"":l.cachedPlaceHolder)},ge=()=>{const n=I.value.filter(r=>r.visible&&!r.disabled&&!r.states.groupDisabled),o=n.find(r=>r.created),a=n[0];l.hoverIndex=de(I.value,o||a)},ue=()=>{var n;if(e.multiple)l.selectedLabel="";else{const a=ye(e.modelValue);(n=a.props)!=null&&n.created?(l.createdLabel=a.props.value,l.createdSelected=!0):l.createdSelected=!1,l.selectedLabel=a.currentLabel,l.selected=a,e.filterable&&(l.query=l.selectedLabel);return}const o=[];Array.isArray(e.modelValue)&&e.modelValue.forEach(a=>{o.push(ye(a))}),l.selected=o,E(()=>{W()})},ye=n=>{let o;const a=ll(n).toLowerCase()==="object",r=ll(n).toLowerCase()==="null",O=ll(n).toLowerCase()==="undefined";for(let R=l.cachedOptions.size-1;R>=0;R--){const V=ze.value[R];if(a?D(V.value,e.valueKey)===D(n,e.valueKey):V.value===n){o={value:n,currentLabel:V.currentLabel,isDisabled:V.isDisabled};break}}if(o)return o;const Q=a?n.label:!r&&!O?n:"",G={value:n,currentLabel:Q};return e.multiple&&(G.hitState=!1),G},Fe=()=>{setTimeout(()=>{const n=e.valueKey;e.multiple?l.selected.length>0?l.hoverIndex=Math.min.apply(null,l.selected.map(o=>I.value.findIndex(a=>D(a,n)===D(o,n)))):l.hoverIndex=-1:l.hoverIndex=I.value.findIndex(o=>pe(o)===pe(l.selected))},300)},We=()=>{var n,o;Ke(),(o=(n=u.value)==null?void 0:n.updatePopper)==null||o.call(n),e.multiple&&!e.filterable&&W()},Ke=()=>{var n;l.inputWidth=(n=d.value)==null?void 0:n.$el.getBoundingClientRect().width},Ae=()=>{e.filterable&&l.query!==l.selectedLabel&&(l.query=l.selectedLabel,H(l.query))},Re=fl(()=>{Ae()},be.value),He=fl(n=>{H(n.target.value)},be.value),X=n=>{pl(e.modelValue,n)||i.emit(Sl,n)},Ne=n=>{if(n.target.value.length<=0&&!ce()){const o=e.modelValue.slice();o.pop(),i.emit(Y,o),X(o)}n.target.value.length===1&&e.modelValue.length===0&&(l.currentPlaceholder=l.cachedPlaceHolder)},je=(n,o)=>{const a=l.selected.indexOf(o);if(a>-1&&!S.value){const r=e.modelValue.slice();r.splice(a,1),i.emit(Y,r),X(r),i.emit("remove-tag",o.value)}n.stopPropagation()},Z=n=>{n.stopPropagation();const o=e.multiple?[]:"";if(!zl(o))for(const a of l.selected)a.isDisabled&&o.push(a.value);i.emit(Y,o),X(o),l.hoverIndex=-1,l.visible=!1,i.emit("clear")},Ce=(n,o)=>{var a;if(e.multiple){const r=(e.modelValue||[]).slice(),O=de(r,n.value);O>-1?r.splice(O,1):(e.multipleLimit<=0||r.length<e.multipleLimit)&&r.push(n.value),i.emit(Y,r),X(r),n.created&&(l.query="",H(""),l.inputLength=20),e.filterable&&((a=s.value)==null||a.focus())}else i.emit(Y,n.value),X(n.value),l.visible=!1;l.isSilentBlur=o,Qe(),!l.visible&&E(()=>{N(n)})},de=(n=[],o)=>{if(!vl(o))return n.indexOf(o);const a=e.valueKey;let r=-1;return n.some((O,Q)=>Ee(D(O,a))===D(o,a)?(r=Q,!0):!1),r},Qe=()=>{l.softFocus=!0;const n=s.value||d.value;n&&(n==null||n.focus())},N=n=>{var o,a,r,O,Q;const G=Array.isArray(n)?n[0]:n;let R=null;if(G!=null&&G.value){const V=I.value.filter(Ie=>Ie.value===G.value);V.length>0&&(R=V[0].$el)}if(u.value&&R){const V=(O=(r=(a=(o=u.value)==null?void 0:o.popperRef)==null?void 0:a.contentRef)==null?void 0:r.querySelector)==null?void 0:O.call(r,`.${m.be("dropdown","wrap")}`);V&&en(V,R)}(Q=v.value)==null||Q.handleScroll()},Ge=n=>{l.optionsCount++,l.filteredOptionsCount++,l.options.set(n.value,n),l.cachedOptions.set(n.value,n)},Ue=(n,o)=>{l.options.get(n)===o&&(l.optionsCount--,l.filteredOptionsCount--,l.options.delete(n))},Je=n=>{n.code!==Bl.backspace&&ce(!1),l.inputLength=s.value.value.length*15+20,W()},ce=n=>{if(!Array.isArray(l.selected))return;const o=l.selected[l.selected.length-1];if(!!o)return n===!0||n===!1?(o.hitState=n,n):(o.hitState=!o.hitState,o.hitState)},Ye=n=>{const o=n.target.value;if(n.type==="compositionend")l.isOnComposition=!1,E(()=>H(o));else{const a=o[o.length-1]||"";l.isOnComposition=!Dl(a)}},Xe=()=>{E(()=>N(l.selected))},j=n=>{l.softFocus?l.softFocus=!1:((e.automaticDropdown||e.filterable)&&(e.filterable&&!l.visible&&(l.menuVisibleOnFocus=!0),l.visible=!0),i.emit("focus",n))},Se=()=>{var n;l.visible=!1,(n=d.value)==null||n.blur()},Ze=n=>{E(()=>{l.isSilentBlur?l.isSilentBlur=!1:i.emit("blur",n)}),l.softFocus=!1},Oe=n=>{Z(n)},xe=()=>{l.visible=!1},_e=n=>{l.visible&&(n.preventDefault(),n.stopPropagation(),l.visible=!1)},we=n=>{var o;n&&!l.mouseEnter||S.value||(l.menuVisibleOnFocus?l.menuVisibleOnFocus=!1:(!u.value||!u.value.isFocusInsideContent())&&(l.visible=!l.visible),l.visible&&((o=s.value||d.value)==null||o.focus()))},Te=()=>{l.visible?I.value[l.hoverIndex]&&Ce(I.value[l.hoverIndex],void 0):we()},pe=n=>vl(n.value)?D(n.value,e.valueKey):n.value,el=c(()=>I.value.filter(n=>n.visible).every(n=>n.disabled)),le=n=>{if(!l.visible){l.visible=!0;return}if(!(l.options.size===0||l.filteredOptionsCount===0)&&!l.isOnComposition&&!el.value){n==="next"?(l.hoverIndex++,l.hoverIndex===l.options.size&&(l.hoverIndex=0)):n==="prev"&&(l.hoverIndex--,l.hoverIndex<0&&(l.hoverIndex=l.options.size-1));const o=I.value[l.hoverIndex];(o.disabled===!0||o.states.groupDisabled===!0||!o.visible)&&le(n),E(()=>N(w.value))}};return{optionsArray:I,selectSize:ee,handleResize:We,debouncedOnInputChange:Re,debouncedQueryChange:He,deletePrevTag:Ne,deleteTag:je,deleteSelected:Z,handleOptionSelect:Ce,scrollToOption:N,readonly:g,resetInputHeight:W,showClose:F,iconComponent:se,iconReverse:ke,showNewOption:Be,collapseTagSize:De,setSelected:ue,managePlaceholder:he,selectDisabled:S,emptyText:re,toggleLastOptionHitState:ce,resetInputState:Je,handleComposition:Ye,onOptionCreate:Ge,onOptionDestroy:Ue,handleMenuEnter:Xe,handleFocus:j,blur:Se,handleBlur:Ze,handleClearClick:Oe,handleClose:xe,handleKeydownEscape:_e,toggleMenu:we,selectOption:Te,getValueKey:pe,navigateOptions:le,dropMenuVisible:qe,queryChange:T,groupQueryChange:M,reference:d,input:s,tooltipRef:u,tags:y,selectWrapper:C,scrollbar:v,handleMouseEnter:()=>{l.mouseEnter=!0},handleMouseLeave:()=>{l.mouseEnter=!1}}},gl="ElSelect",fn=Me({name:gl,componentName:gl,components:{ElInput:ql,ElSelectMenu:dn,ElOption:rl,ElTag:Fl,ElScrollbar:Wl,ElTooltip:Kl,ElIcon:Al},directives:{ClickOutside:Rl},props:{name:String,id:String,modelValue:{type:[Array,String,Number,Boolean,Object],default:void 0},autocomplete:{type:String,default:"off"},automaticDropdown:Boolean,size:{type:String,validator:nn},effect:{type:String,default:"light"},disabled:Boolean,clearable:Boolean,filterable:Boolean,allowCreate:Boolean,loading:Boolean,popperClass:{type:String,default:""},remote:Boolean,loadingText:String,noMatchText:String,noDataText:String,remoteMethod:Function,filterMethod:Function,multiple:Boolean,multipleLimit:{type:Number,default:0},placeholder:{type:String},defaultFirstOption:Boolean,reserveKeyword:{type:Boolean,default:!0},valueKey:{type:String,default:"value"},collapseTags:Boolean,collapseTagsTooltip:{type:Boolean,default:!1},teleported:Hl.teleported,persistent:{type:Boolean,default:!0},clearIcon:{type:ml,default:Nl},fitInputWidth:{type:Boolean,default:!1},suffixIcon:{type:ml,default:jl},tagType:{...Ql.type,default:"info"},validateEvent:{type:Boolean,default:!0},remoteShowSuffix:{type:Boolean,default:!1},suffixTransition:{type:Boolean,default:!0},placement:{type:String,values:Gl,default:"bottom-start"}},emits:[Y,Sl,"remove-tag","clear","visible-change","focus","blur"],setup(e,l){const i=ae("select"),p=ae("input"),{t:m}=sl(),d=cn(e),{optionsArray:s,selectSize:u,readonly:y,handleResize:C,collapseTagSize:v,debouncedOnInputChange:w,debouncedQueryChange:T,deletePrevTag:M,deleteTag:t,deleteSelected:f,handleOptionSelect:g,scrollToOption:S,setSelected:F,resetInputHeight:se,managePlaceholder:ke,showClose:be,selectDisabled:re,iconComponent:I,iconReverse:ze,showNewOption:Be,emptyText:ee,toggleLastOptionHitState:De,resetInputState:qe,handleComposition:W,onOptionCreate:H,onOptionDestroy:he,handleMenuEnter:ge,handleFocus:ue,blur:ye,handleBlur:Fe,handleClearClick:We,handleClose:Ke,handleKeydownEscape:Ae,toggleMenu:Re,selectOption:He,getValueKey:X,navigateOptions:Ne,dropMenuVisible:je,reference:Z,input:Ce,tooltipRef:de,tags:Qe,selectWrapper:N,scrollbar:Ge,queryChange:Ue,groupQueryChange:Je,handleMouseEnter:ce,handleMouseLeave:Ye}=pn(e,d,l),{focus:Xe}=on(Z),{inputWidth:j,selected:Se,inputLength:Ze,filteredOptionsCount:Oe,visible:xe,softFocus:_e,selectedLabel:we,hoverIndex:Te,query:pe,inputHovering:el,currentPlaceholder:le,menuVisibleOnFocus:ul,isOnComposition:dl,isSilentBlur:n,options:o,cachedOptions:a,optionsCount:r,prefixWidth:O,tagInMultiLine:Q}=tl(d),G=c(()=>{const k=[i.b()],x=oe(u);return x&&k.push(i.m(x)),e.disabled&&k.push(i.m("disabled")),k}),R=c(()=>({maxWidth:`${oe(j)-32}px`,width:"100%"})),V=c(()=>({maxWidth:`${oe(j)>123?oe(j)-123:oe(j)-75}px`}));Ol(Pe,$e({props:e,options:o,optionsArray:s,cachedOptions:a,optionsCount:r,filteredOptionsCount:Oe,hoverIndex:Te,handleOptionSelect:g,onOptionCreate:H,onOptionDestroy:he,selectWrapper:N,selected:Se,setSelected:F,queryChange:Ue,groupQueryChange:Je})),al(()=>{d.cachedPlaceHolder=le.value=e.placeholder||m("el.select.placeholder"),e.multiple&&Array.isArray(e.modelValue)&&e.modelValue.length>0&&(le.value=""),Cl(N,C),e.remote&&e.multiple&&se(),E(()=>{const k=Z.value&&Z.value.$el;if(!!k&&(j.value=k.getBoundingClientRect().width,l.slots.prefix)){const x=k.querySelector(`.${p.e("prefix")}`);O.value=Math.max(x.getBoundingClientRect().width+5,30)}}),F()}),e.multiple&&!Array.isArray(e.modelValue)&&l.emit(Y,[]),!e.multiple&&Array.isArray(e.modelValue)&&l.emit(Y,"");const Ie=c(()=>{var k,x;return(x=(k=de.value)==null?void 0:k.popperRef)==null?void 0:x.contentRef});return{tagInMultiLine:Q,prefixWidth:O,selectSize:u,readonly:y,handleResize:C,collapseTagSize:v,debouncedOnInputChange:w,debouncedQueryChange:T,deletePrevTag:M,deleteTag:t,deleteSelected:f,handleOptionSelect:g,scrollToOption:S,inputWidth:j,selected:Se,inputLength:Ze,filteredOptionsCount:Oe,visible:xe,softFocus:_e,selectedLabel:we,hoverIndex:Te,query:pe,inputHovering:el,currentPlaceholder:le,menuVisibleOnFocus:ul,isOnComposition:dl,isSilentBlur:n,options:o,resetInputHeight:se,managePlaceholder:ke,showClose:be,selectDisabled:re,iconComponent:I,iconReverse:ze,showNewOption:Be,emptyText:ee,toggleLastOptionHitState:De,resetInputState:qe,handleComposition:W,handleMenuEnter:ge,handleFocus:ue,blur:ye,handleBlur:Fe,handleClearClick:We,handleClose:Ke,handleKeydownEscape:Ae,toggleMenu:Re,selectOption:He,getValueKey:X,navigateOptions:Ne,dropMenuVisible:je,focus:Xe,reference:Z,input:Ce,tooltipRef:de,popperPaneRef:Ie,tags:Qe,selectWrapper:N,scrollbar:Ge,wrapperKls:G,selectTagsStyle:R,nsSelect:i,tagTextStyle:V,handleMouseEnter:ce,handleMouseLeave:Ye}}}),vn=["disabled","autocomplete"],mn={style:{height:"100%",display:"flex","justify-content":"center","align-items":"center"}};function bn(e,l,i,p,m,d){const s=_("el-tag"),u=_("el-tooltip"),y=_("el-icon"),C=_("el-input"),v=_("el-option"),w=_("el-scrollbar"),T=_("el-select-menu"),M=Ul("click-outside");return me((b(),$("div",{ref:"selectWrapper",class:h(e.wrapperKls),onMouseenter:l[22]||(l[22]=(...t)=>e.handleMouseEnter&&e.handleMouseEnter(...t)),onMouseleave:l[23]||(l[23]=(...t)=>e.handleMouseLeave&&e.handleMouseLeave(...t)),onClick:l[24]||(l[24]=U((...t)=>e.toggleMenu&&e.toggleMenu(...t),["stop"]))},[ve(u,{ref:"tooltipRef",visible:e.dropMenuVisible,placement:e.placement,teleported:e.teleported,"popper-class":[e.nsSelect.e("popper"),e.popperClass],"fallback-placements":["bottom-start","top-start","right","left"],effect:e.effect,pure:"",trigger:"click",transition:`${e.nsSelect.namespace.value}-zoom-in-top`,"stop-popper-mouse-event":!1,"gpu-acceleration":!1,persistent:e.persistent,onShow:e.handleMenuEnter},{default:L(()=>[P("div",{class:"select-trigger",onMouseenter:l[20]||(l[20]=t=>e.inputHovering=!0),onMouseleave:l[21]||(l[21]=t=>e.inputHovering=!1)},[e.multiple?(b(),$("div",{key:0,ref:"tags",class:h(e.nsSelect.e("tags")),style:te(e.selectTagsStyle)},[e.collapseTags&&e.selected.length?(b(),$("span",{key:0,class:h([e.nsSelect.b("tags-wrapper"),{"has-prefix":e.prefixWidth&&e.selected.length}])},[ve(s,{closable:!e.selectDisabled&&!e.selected[0].isDisabled,size:e.collapseTagSize,hit:e.selected[0].hitState,type:e.tagType,"disable-transitions":"",onClose:l[0]||(l[0]=t=>e.deleteTag(t,e.selected[0]))},{default:L(()=>[P("span",{class:h(e.nsSelect.e("tags-text")),style:te(e.tagTextStyle)},J(e.selected[0].currentLabel),7)]),_:1},8,["closable","size","hit","type"]),e.selected.length>1?(b(),K(s,{key:0,closable:!1,size:e.collapseTagSize,type:e.tagType,"disable-transitions":""},{default:L(()=>[e.collapseTagsTooltip?(b(),K(u,{key:0,disabled:e.dropMenuVisible,"fallback-placements":["bottom","top","right","left"],effect:e.effect,placement:"bottom",teleported:e.teleported},{default:L(()=>[P("span",{class:h(e.nsSelect.e("tags-text"))},"+ "+J(e.selected.length-1),3)]),content:L(()=>[P("div",{class:h(e.nsSelect.e("collapse-tags"))},[(b(!0),$(nl,null,bl(e.selected.slice(1),(t,f)=>(b(),$("div",{key:f,class:h(e.nsSelect.e("collapse-tag"))},[(b(),K(s,{key:e.getValueKey(t),class:"in-tooltip",closable:!e.selectDisabled&&!t.isDisabled,size:e.collapseTagSize,hit:t.hitState,type:e.tagType,"disable-transitions":"",style:{margin:"2px"},onClose:g=>e.deleteTag(g,t)},{default:L(()=>[P("span",{class:h(e.nsSelect.e("tags-text")),style:te({maxWidth:e.inputWidth-75+"px"})},J(t.currentLabel),7)]),_:2},1032,["closable","size","hit","type","onClose"]))],2))),128))],2)]),_:1},8,["disabled","effect","teleported"])):(b(),$("span",{key:1,class:h(e.nsSelect.e("tags-text"))},"+ "+J(e.selected.length-1),3))]),_:1},8,["size","type"])):z("v-if",!0)],2)):z("v-if",!0),z(" <div> "),e.collapseTags?z("v-if",!0):(b(),K(Jl,{key:1,onAfterLeave:e.resetInputHeight},{default:L(()=>[P("span",{class:h([e.nsSelect.b("tags-wrapper"),{"has-prefix":e.prefixWidth&&e.selected.length}])},[(b(!0),$(nl,null,bl(e.selected,t=>(b(),K(s,{key:e.getValueKey(t),closable:!e.selectDisabled&&!t.isDisabled,size:e.collapseTagSize,hit:t.hitState,type:e.tagType,"disable-transitions":"",onClose:f=>e.deleteTag(f,t)},{default:L(()=>[P("span",{class:h(e.nsSelect.e("tags-text")),style:te({maxWidth:e.inputWidth-75+"px"})},J(t.currentLabel),7)]),_:2},1032,["closable","size","hit","type","onClose"]))),128))],2)]),_:1},8,["onAfterLeave"])),z(" </div> "),e.filterable?me((b(),$("input",{key:2,ref:"input","onUpdate:modelValue":l[1]||(l[1]=t=>e.query=t),type:"text",class:h([e.nsSelect.e("input"),e.nsSelect.is(e.selectSize)]),disabled:e.selectDisabled,autocomplete:e.autocomplete,style:te({marginLeft:e.prefixWidth&&!e.selected.length||e.tagInMultiLine?`${e.prefixWidth}px`:"",flexGrow:1,width:`${e.inputLength/(e.inputWidth-32)}%`,maxWidth:`${e.inputWidth-42}px`}),onFocus:l[2]||(l[2]=(...t)=>e.handleFocus&&e.handleFocus(...t)),onBlur:l[3]||(l[3]=(...t)=>e.handleBlur&&e.handleBlur(...t)),onKeyup:l[4]||(l[4]=(...t)=>e.managePlaceholder&&e.managePlaceholder(...t)),onKeydown:[l[5]||(l[5]=(...t)=>e.resetInputState&&e.resetInputState(...t)),l[6]||(l[6]=B(U(t=>e.navigateOptions("next"),["prevent"]),["down"])),l[7]||(l[7]=B(U(t=>e.navigateOptions("prev"),["prevent"]),["up"])),l[8]||(l[8]=B((...t)=>e.handleKeydownEscape&&e.handleKeydownEscape(...t),["esc"])),l[9]||(l[9]=B(U((...t)=>e.selectOption&&e.selectOption(...t),["stop","prevent"]),["enter"])),l[10]||(l[10]=B((...t)=>e.deletePrevTag&&e.deletePrevTag(...t),["delete"])),l[11]||(l[11]=B(t=>e.visible=!1,["tab"]))],onCompositionstart:l[12]||(l[12]=(...t)=>e.handleComposition&&e.handleComposition(...t)),onCompositionupdate:l[13]||(l[13]=(...t)=>e.handleComposition&&e.handleComposition(...t)),onCompositionend:l[14]||(l[14]=(...t)=>e.handleComposition&&e.handleComposition(...t)),onInput:l[15]||(l[15]=(...t)=>e.debouncedQueryChange&&e.debouncedQueryChange(...t))},null,46,vn)),[[Yl,e.query]]):z("v-if",!0)],6)):z("v-if",!0),ve(C,{id:e.id,ref:"reference",modelValue:e.selectedLabel,"onUpdate:modelValue":l[16]||(l[16]=t=>e.selectedLabel=t),type:"text",placeholder:e.currentPlaceholder,name:e.name,autocomplete:e.autocomplete,size:e.selectSize,disabled:e.selectDisabled,readonly:e.readonly,"validate-event":!1,class:h([e.nsSelect.is("focus",e.visible)]),tabindex:e.multiple&&e.filterable?-1:void 0,onFocus:e.handleFocus,onBlur:e.handleBlur,onInput:e.debouncedOnInputChange,onPaste:e.debouncedOnInputChange,onCompositionstart:e.handleComposition,onCompositionupdate:e.handleComposition,onCompositionend:e.handleComposition,onKeydown:[l[17]||(l[17]=B(U(t=>e.navigateOptions("next"),["stop","prevent"]),["down"])),l[18]||(l[18]=B(U(t=>e.navigateOptions("prev"),["stop","prevent"]),["up"])),B(U(e.selectOption,["stop","prevent"]),["enter"]),B(e.handleKeydownEscape,["esc"]),l[19]||(l[19]=B(t=>e.visible=!1,["tab"]))]},Xl({suffix:L(()=>[e.iconComponent&&!e.showClose?(b(),K(y,{key:0,class:h([e.nsSelect.e("caret"),e.nsSelect.e("icon"),e.iconReverse])},{default:L(()=>[(b(),K(hl(e.iconComponent)))]),_:1},8,["class"])):z("v-if",!0),e.showClose&&e.clearIcon?(b(),K(y,{key:1,class:h([e.nsSelect.e("caret"),e.nsSelect.e("icon")]),onClick:e.handleClearClick},{default:L(()=>[(b(),K(hl(e.clearIcon)))]),_:1},8,["class","onClick"])):z("v-if",!0)]),_:2},[e.$slots.prefix?{name:"prefix",fn:L(()=>[P("div",mn,[ie(e.$slots,"prefix")])])}:void 0]),1032,["id","modelValue","placeholder","name","autocomplete","size","disabled","readonly","class","tabindex","onFocus","onBlur","onInput","onPaste","onCompositionstart","onCompositionupdate","onCompositionend","onKeydown"])],32)]),content:L(()=>[ve(T,null,{default:L(()=>[me(ve(w,{ref:"scrollbar",tag:"ul","wrap-class":e.nsSelect.be("dropdown","wrap"),"view-class":e.nsSelect.be("dropdown","list"),class:h([e.nsSelect.is("empty",!e.allowCreate&&Boolean(e.query)&&e.filteredOptionsCount===0)])},{default:L(()=>[e.showNewOption?(b(),K(v,{key:0,value:e.query,created:!0},null,8,["value"])):z("v-if",!0),ie(e.$slots,"default")]),_:3},8,["wrap-class","view-class","class"]),[[il,e.options.size>0&&!e.loading]]),e.emptyText&&(!e.allowCreate||e.loading||e.allowCreate&&e.options.size===0)?(b(),$(nl,{key:0},[e.$slots.empty?ie(e.$slots,"empty",{key:0}):(b(),$("p",{key:1,class:h(e.nsSelect.be("dropdown","empty"))},J(e.emptyText),3))],64)):z("v-if",!0)]),_:3})]),_:3},8,["visible","placement","teleported","popper-class","effect","transition","persistent","onShow"])],34)),[[M,e.handleClose,e.popperPaneRef]])}var hn=Ve(fn,[["render",bn],["__file","/home/runner/work/element-plus/element-plus/packages/components/select/src/select.vue"]]);const gn=Me({name:"ElOptionGroup",componentName:"ElOptionGroup",props:{label:String,disabled:{type:Boolean,default:!1}},setup(e){const l=ae("select"),i=A(!0),p=ol(),m=A([]);Ol(Tl,$e({...tl(e)}));const d=Le(Pe);al(()=>{m.value=s(p.subTree)});const s=y=>{const C=[];return Array.isArray(y.children)&&y.children.forEach(v=>{var w;v.type&&v.type.name==="ElOption"&&v.component&&v.component.proxy?C.push(v.component.proxy):(w=v.children)!=null&&w.length&&C.push(...s(v))}),C},{groupQueryChange:u}=Ee(d);return q(u,()=>{i.value=m.value.some(y=>y.visible===!0)},{flush:"post"}),{visible:i,ns:l}}});function yn(e,l,i,p,m,d){return me((b(),$("ul",{class:h(e.ns.be("group","wrap"))},[P("li",{class:h(e.ns.be("group","title"))},J(e.label),3),P("li",null,[P("ul",{class:h(e.ns.b("group"))},[ie(e.$slots,"default")],2)])],2)),[[il,e.visible]])}var Il=Ve(gn,[["render",yn],["__file","/home/runner/work/element-plus/element-plus/packages/components/select/src/option-group.vue"]]);const On=Zl(hn,{Option:rl,OptionGroup:Il}),wn=wl(rl);wl(Il);export{wn as E,On as a};
