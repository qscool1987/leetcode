import{aL as u,r as m,z as p,I as f,Z as a,B as n,U as i,W as B,bt as k}from"./index.eddadff6.js";import{E as x,a as F,b as v}from"./el-form-item.20795bea.js";const g={__name:"FeedBack",setup(I){const t=m(""),l=()=>{s()},s=()=>{if(t.value===""){alert("\u53CD\u9988\u4FE1\u606F\u4E0D\u80FD\u4E3A\u7A7A!");return}const o={msg:t.value};k.getFeedBackInfo(o).then(e=>{console.log(e.data),e.data[0]===0?alert("\u53CD\u9988\u6210\u529F!"):alert(e.data[1])})};return(o,e)=>{const c=x,_=F,d=v;return p(),f(i,null,[a(c,{modelValue:t.value,"onUpdate:modelValue":e[0]||(e[0]=r=>t.value=r),autosize:{minRows:5,maxRows:10},type:"textarea",placeholder:"\u610F\u89C1\u53CD\u9988"},null,8,["modelValue"]),a(d,null,{default:n(()=>[a(_,{type:"primary",onClick:l},{default:n(()=>[B("\u63D0\u4EA4\u610F\u89C1")]),_:1})]),_:1})],64)}}},V=u(g,[["__scopeId","data-v-9d312fdf"]]);export{V as default};