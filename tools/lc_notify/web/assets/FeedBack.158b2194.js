import{aQ as p,r as f,F as i,C as s,M as k,a0 as t,E as o,Y as B,W as x,bq as F,D as b,aR as v}from"./index.4d31215e.js";import{E,a as I}from"./el-form-item.5592b24f.js";const g={__name:"FeedBack",setup(l){const a=f(""),n=()=>{_()},_=()=>{if(a.value===""){alert("\u53CD\u9988\u4FE1\u606F\u4E0D\u80FD\u4E3A\u7A7A!");return}const c={msg:a.value};F.submitFeedBackInfo(c).then(e=>{console.log(e.data),e.data[0]===0?alert("\u53CD\u9988\u6210\u529F!"):alert(e.data[1])})};return(c,e)=>{const r=i,u=E,d=I;return s(),k(x,null,[t(r,{modelValue:a.value,"onUpdate:modelValue":e[0]||(e[0]=m=>a.value=m),autosize:{minRows:5,maxRows:10},type:"textarea",placeholder:"\u610F\u89C1\u53CD\u9988"},null,8,["modelValue"]),t(d,null,{default:o(()=>[t(u,{type:"primary",onClick:n},{default:o(()=>[B("\u63D0\u4EA4\u610F\u89C1")]),_:1})]),_:1})],64)}}},y=p(g,[["__scopeId","data-v-5bc5fa7a"]]),w={__name:"FeedBack",setup(l){return(a,n)=>(s(),b(v,null,{feed_back:o(()=>[t(y)]),_:1}))}};export{w as default};
