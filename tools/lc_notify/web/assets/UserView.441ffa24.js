import{au as b,n as i,p as d,w as a,x as t,G as f,aC as V,J as x}from"./index.6b5dcf9f.js";import{E as h,a as g}from"./el-form-item.b08c5ac6.js";import{E}from"./el-button.20a13a44.js";import"./index.a50b6ef4.js";const U={__name:"BindForm",setup(s){const e=b({leetcode:"",github:"",email:""}),m=()=>{c()},c=()=>{if(e.leetcode===""){alert("LeetCode\u8D26\u6237\u4E0D\u80FD\u4E3A\u7A7A!");return}const u={lc_account:e.leetcode,git_account:e.github,email_account:e.email};V.submitUser(u).then(l=>{l.data[0]===0?alert("\u6DFB\u52A0\u6210\u529F!"):alert(l.data[1])})};return(u,l)=>{const r=x,n=h,p=E,_=g;return i(),d(_,{"label-position":"top","label-width":"110px",model:e,style:{"max-width":"300px"},class:"mx-auto"},{default:a(()=>[t(n,{label:"LeetCode\u8D26\u53F7",required:!0},{default:a(()=>[t(r,{modelValue:e.leetcode,"onUpdate:modelValue":l[0]||(l[0]=o=>e.leetcode=o),placeholder:"\u8BF7\u8F93\u5165LeetCode\u8D26\u53F7",clearable:""},null,8,["modelValue"])]),_:1}),t(n,{label:"Github\u8D26\u53F7"},{default:a(()=>[t(r,{modelValue:e.github,"onUpdate:modelValue":l[1]||(l[1]=o=>e.github=o),placeholder:"\u8BF7\u8F93\u5165Github\u7528\u6237\u540D",clearable:""},null,8,["modelValue"])]),_:1}),t(n,{label:"\u90AE\u7BB1\u8D26\u53F7"},{default:a(()=>[t(r,{type:"email",modelValue:e.email,"onUpdate:modelValue":l[2]||(l[2]=o=>e.email=o),placeholder:"Email",clearable:""},null,8,["modelValue"])]),_:1}),t(n,null,{default:a(()=>[t(p,{type:"primary",onClick:m},{default:a(()=>[f("\u63D0\u4EA4\u7ED1\u5B9A")]),_:1})]),_:1})]),_:1},8,["model"])}}},L={__name:"UserView",setup(s){return(e,m)=>(i(),d(U))}};export{L as default};
