import{aB as k,at as F,bv as y,aD as V,aw as w,n as a,p as m,w as d,x as p,t as l,y as _,F as f,B as g,q as c,G as I,H as v,aE as B}from"./index.015e7807.js";/* empty css                */import{E as S,a as L}from"./el-form-item.b6f27fc7.js";import{E as O,a as $}from"./el-select.d3f8600d.js";const x=k("interview",()=>{const t=F({username:"",typeInfo:[],value:"",titleInfo:[],titleInfoType:[]});return{formLabelAlign:t,getInterviewTitle:()=>{const s={pn:1,rn:1e3};y.getInterviewTitle(s).then(i=>{t.titleInfo=i.data})},getInterviewType:()=>{y.getInterviewType().then(s=>{t.typeInfo=s.data})},selectOne:s=>{t.titleInfoType=t.titleInfo.filter(i=>i.type===s)}}});const A={__name:"InterviewForm",setup(t){const o=x(),{formLabelAlign:e}=w(o),{getInterviewType:u,selectOne:s}=o;return u(),(i,n)=>{const b=O,h=$,T=S,E=L;return a(),m(E,{"label-position":"left",model:l(e)},{default:d(()=>[p(T,{label:"\u9898\u578B\u9009\u62E9"},{default:d(()=>[p(h,{modelValue:l(e).value,"onUpdate:modelValue":n[0]||(n[0]=r=>l(e).value=r),"value-key":l(e).value,class:"m-2",placeholder:"\u8BF7\u9009\u62E9\u9898\u578B",onChange:n[1]||(n[1]=r=>l(s)(l(e).value))},{default:d(()=>[(a(!0),_(f,null,g(l(e).typeInfo,r=>(a(),m(b,{key:r.name,label:r.name,value:r.name},null,8,["label","value"]))),128))]),_:1},8,["modelValue","value-key"])]),_:1})]),_:1},8,["model"])}}},N=V(A,[["__scopeId","data-v-0b244b0b"]]),C={role:"list",class:"divide-y divide-gray-200"},D={class:"bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200"},q={class:"px-4 py-5 sm:px-6"},G=c("br",null,null,-1),H=c("div",{class:"px-4 py-5 sm:p-6"}," \u4F5C\u7B54\u533A\u57DF ",-1),P={class:"px-4 py-4 sm:px-6"},R={__name:"InterviewTitle",setup(t){const o=x(),{formLabelAlign:e}=w(o),{getInterviewTitle:u}=o;return u(),console.log(e.value),(s,i)=>(a(),_("ul",C,[(a(!0),_(f,null,g(l(e).titleInfoType,n=>(a(),_("li",{key:n.type,class:"px-4 py-4 sm:px-0"},[c("div",D,[c("div",q,[I(" \u4F01\u4E1A\uFF1A"+v(n.company)+" ",1),G,I(" \u9898\u76EE\uFF1A"+v(n.content),1)]),H,c("div",P,v(n.type)+" \u63D0\u4EA4\u533A\u57DF ",1)])]))),128))]))}},U={__name:"TheInterview",setup(t){return(o,e)=>(a(),_(f,null,[p(N),p(R)],64))}},M={__name:"VirtualInterview",setup(t){return(o,e)=>(a(),m(B,null,{the_interview:d(()=>[p(U)]),_:1}))}};export{M as default};
