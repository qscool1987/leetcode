import{aB as S,au as g,bv as I,aD as C,aw as x,n as r,p as f,w as d,t as s,x as i,y as m,B as h,F as y,r as F,bw as V,ay as B,q as u,H as v,G as w}from"./index.6fe9a912.js";/* empty css                */import{E as H,a as L}from"./el-form-item.cbc18c2a.js";import{E as O,a as $}from"./el-select.7e515a2e.js";const T=S("interview",()=>{const o=g({username:"",typeInfo:[],value:"",titleInfo:[],titleInfoType:[],textarea:""});return{formLabelAlign:o,getInterviewTitle:()=>{const n={pn:1,rn:1e3};I.getInterviewTitle(n).then(l=>{o.titleInfo=l.data})},getInterviewType:()=>{I.getInterviewType().then(n=>{o.typeInfo=n.data})},selectOne:n=>{o.titleInfoType=o.titleInfo.filter(l=>l.type===n)}}});const A={__name:"InterviewForm",setup(o){const t=T(),{formLabelAlign:e}=x(t),{getInterviewType:c,selectOne:n}=t;return c(),(l,a)=>{const p=O,b=$,k=H,E=L;return r(),f(E,{"label-position":"left",model:s(e)},{default:d(()=>[i(k,{label:"\u9898\u578B\u9009\u62E9"},{default:d(()=>[i(b,{modelValue:s(e).value,"onUpdate:modelValue":a[0]||(a[0]=_=>s(e).value=_),"value-key":s(e).value,class:"m-2",placeholder:"\u8BF7\u9009\u62E9\u9898\u578B",onChange:a[1]||(a[1]=_=>s(n)(s(e).value))},{default:d(()=>[(r(!0),m(y,null,h(s(e).typeInfo,_=>(r(),f(p,{key:_.type,label:_.name,value:_.name},null,8,["label","value"]))),128))]),_:1},8,["modelValue","value-key"])]),_:1})]),_:1},8,["model"])}}},N=C(A,[["__scopeId","data-v-c0575141"]]),W={__name:"CodeEditor",setup(o){const t=F(`/* C */
printf("Hello World!");

/* C++ */
cout << "Hello World!" << endl;

/* Java */
System.out.println("Hello, world!");

/* Python */
print("Hello World!")

/* JavaScript */
console.log('Hello World!')`),e=g({mode:"text/javascript",theme:"default",lineNumbers:!0,smartIndent:!0,indentUnit:2,foldGutter:!0,styleActiveLine:!0}),c=(n,l)=>{};return(n,l)=>(r(),f(s(V),{value:t.value,"onUpdate:value":l[0]||(l[0]=a=>t.value=a),options:e,border:"",placeholder:"test placeholder",height:300,onChange:c},null,8,["value","options"]))}},U={role:"list",class:"divide-y divide-gray-200"},D={class:"bg-white overflow-hidden"},G={class:"px-4 py-1 sm:px-6 flex"},J={class:"px-4 py-5 sm:p-6"},j=u("div",{class:"px-4 py-4 sm:px-6"},null,-1),q={__name:"InterviewTitle",setup(o){const t=T(),{formLabelAlign:e}=x(t),{getInterviewTitle:c}=t;return c(),(n,l)=>{const a=B;return r(),m("ul",U,[(r(!0),m(y,null,h(s(e).titleInfoType,p=>(r(),m("li",{key:p.type,class:"px-4 py-4 sm:px-0"},[u("div",D,[u("div",G,[u("div",null,v(p.content),1),i(a,{type:"",class:"mx-1",effect:"dark",round:""},{default:d(()=>[w(v(p.company),1)]),_:2},1024),i(a,{type:"warning",class:"mx-1",effect:"dark",round:""},{default:d(()=>[w(" #"+v(p.type),1)]),_:2},1024)]),u("div",J,[i(W)]),j])]))),128))])}}},M={__name:"InterviewView",setup(o){return(t,e)=>(r(),m(y,null,[i(N),i(q)],64))}};export{M as default};
