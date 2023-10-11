import{aD as C,bv as h,aw as g,m as F,n as a,p as f,w as _,t,x as c,y as p,B as w,q as r,H as i,F as y,r as T,au as V,bw as $,ay as H,G as x}from"./index.8b2b1f93.js";import{E as S,a as B}from"./el-form-item.454eb660.js";import{E as N,a as L}from"./el-select.bcb2b244.js";import"./index.cde46810.js";const W={style:{float:"left"}},A={style:{float:"right",color:"var(--el-text-color-secondary)","font-size":"13px"}},O={__name:"InterviewForm",setup(m){const o=h(),{formLabelAlign:e}=g(o),{getInterviewTitle:v,getInterviewType:d,selectOne:n,titleNum:l}=o;return F(()=>{d()}),(P,u)=>{const I=N,b=L,k=S,E=B;return a(),f(E,{"label-position":"left",model:t(e)},{default:_(()=>[c(k,{label:"\u9898\u578B\u9009\u62E9"},{default:_(()=>[c(b,{modelValue:t(e).value,"onUpdate:modelValue":u[0]||(u[0]=s=>t(e).value=s),"value-key":t(e).value,class:"m-2",placeholder:"\u8BF7\u9009\u62E9\u9898\u578B",onChange:u[1]||(u[1]=s=>t(n)(t(e).value))},{default:_(()=>[(a(!0),p(y,null,w(t(e).typeInfo,s=>(a(),f(I,{key:s.type,label:s.name,value:s.name},{default:_(()=>[r("span",W,i(s.name),1),r("span",A,i(t(l)(s.name)),1)]),_:2},1032,["label","value"]))),128))]),_:1},8,["modelValue","value-key"])]),_:1})]),_:1},8,["model"])}}},U=C(O,[["__scopeId","data-v-4e2895c8"]]),D={__name:"CodeEditor",setup(m){const o=T(`/* C */
printf("Hello World!");

/* C++ */
cout << "Hello World!" << endl;

/* Java */
System.out.println("Hello, world!");

/* Python */
print("Hello World!")

/* JavaScript */
console.log('Hello World!')`),e=V({mode:"text/javascript",theme:"default",lineNumbers:!0,smartIndent:!0,indentUnit:2,foldGutter:!0,styleActiveLine:!0}),v=(d,n)=>{};return(d,n)=>(a(),f(t($),{value:o.value,"onUpdate:value":n[0]||(n[0]=l=>o.value=l),options:e,border:"",placeholder:"test placeholder",height:300,onChange:v},null,8,["value","options"]))}},G={role:"list",class:"divide-y divide-gray-200"},J={class:"bg-white overflow-hidden"},j={class:"px-4 py-1 sm:px-6 flex"},q={class:"px-4 py-5 sm:p-6"},z=r("div",{class:"px-4 py-4 sm:px-6"},null,-1),M={__name:"InterviewTitle",setup(m){const o=h(),{formLabelAlign:e}=g(o);return(v,d)=>{const n=H;return a(),p("ul",G,[(a(!0),p(y,null,w(t(e).titleInfoType,l=>(a(),p("li",{key:l.type,class:"px-4 py-4 sm:px-0"},[r("div",J,[r("div",j,[r("div",null,i(l.content),1),c(n,{type:"",class:"mx-1",effect:"dark",round:""},{default:_(()=>[x(i(l.company),1)]),_:2},1024),c(n,{type:"warning",class:"mx-1",effect:"dark",round:""},{default:_(()=>[x(" #"+i(l.type),1)]),_:2},1024)]),r("div",q,[c(D)]),z])]))),128))])}}},Y={__name:"InterviewView",setup(m){return(o,e)=>(a(),p(y,null,[c(U),c(M)],64))}};export{Y as default};
