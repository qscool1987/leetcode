import{aB as b,at as k,bv as I,aD as F,aw as g,n as r,p as w,w as _,x as i,t,y as m,F as T,B as h,ay as B,J as S,q as u,H as y,G as x,aE as L}from"./index.fa7d4eab.js";/* empty css                */import{E as O,a as A}from"./el-form-item.2a6ffedb.js";import{E as N,a as R}from"./el-select.4e12bc5f.js";const E=b("interview",()=>{const n=k({username:"",typeInfo:[],value:"",titleInfo:[],titleInfoType:[],textarea:""});return{formLabelAlign:n,getInterviewTitle:()=>{const o={pn:1,rn:1e3};I.getInterviewTitle(o).then(l=>{n.titleInfo=l.data})},getInterviewType:()=>{I.getInterviewType().then(o=>{n.typeInfo=o.data})},selectOne:o=>{n.titleInfoType=n.titleInfo.filter(l=>l.type===o)}}});const $={__name:"InterviewForm",setup(n){const a=E(),{formLabelAlign:e}=g(a),{getInterviewType:d,selectOne:o}=a;return d(),(l,s)=>{const v=N,c=R,f=O,V=A;return r(),w(V,{"label-position":"left",model:t(e)},{default:_(()=>[i(f,{label:"\u9898\u578B\u9009\u62E9"},{default:_(()=>[i(c,{modelValue:t(e).value,"onUpdate:modelValue":s[0]||(s[0]=p=>t(e).value=p),"value-key":t(e).value,class:"m-2",placeholder:"\u8BF7\u9009\u62E9\u9898\u578B",onChange:s[1]||(s[1]=p=>t(o)(t(e).value))},{default:_(()=>[(r(!0),m(T,null,h(t(e).typeInfo,p=>(r(),w(v,{key:p.type,label:p.name,value:p.name},null,8,["label","value"]))),128))]),_:1},8,["modelValue","value-key"])]),_:1})]),_:1},8,["model"])}}},C=F($,[["__scopeId","data-v-c0575141"]]),D={role:"list",class:"divide-y divide-gray-200"},U={class:"bg-white overflow-hidden"},q={class:"px-4 py-1 sm:px-6 flex"},z={class:"px-4 py-5 sm:p-6"},G=u("div",{class:"px-4 py-4 sm:px-6"},null,-1),H={__name:"InterviewTitle",setup(n){const a=E(),{formLabelAlign:e}=g(a),{getInterviewTitle:d}=a;return d(),(o,l)=>{const s=B,v=S;return r(),m("ul",D,[(r(!0),m(T,null,h(t(e).titleInfoType,c=>(r(),m("li",{key:c.type,class:"px-4 py-4 sm:px-0"},[u("div",U,[u("div",q,[u("div",null,y(c.content),1),i(s,{type:"",class:"mx-1",effect:"dark",round:""},{default:_(()=>[x(y(c.company),1)]),_:2},1024),i(s,{type:"warning",class:"mx-1",effect:"dark",round:""},{default:_(()=>[x(" #"+y(c.type),1)]),_:2},1024)]),u("div",z,[i(v,{modelValue:t(e).textarea,"onUpdate:modelValue":l[0]||(l[0]=f=>t(e).textarea=f),autosize:{minRows:10,maxRows:100},type:"textarea",placeholder:"\u4F5C\u7B54\u533A\u57DF"},null,8,["modelValue"])]),G])]))),128))])}}},M={__name:"InterviewView",setup(n){return(a,e)=>(r(),w(L,null,{interview_view:_(()=>[i(C),i(H)]),_:1}))}};export{M as default};
