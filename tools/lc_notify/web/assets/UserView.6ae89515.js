import{au as b,n as d,p as s,w as o,x as l,G as i,aC as h,J as V}from"./index.71eb32e1.js";/* empty css                */import{E as g}from"./el-button.50dd6e81.js";import{E as x,a as E}from"./el-form-item.9c43c225.js";const U={__name:"BindForm",setup(c){const e=b({leetcode:"",github:"",email:""}),u=()=>{p()},p=()=>{if(e.leetcode===""){alert("LeetCode\u8D26\u6237\u4E0D\u80FD\u4E3A\u7A7A!");return}const r={lc_account:e.leetcode,git_account:"https://github.com/"+e.github,email_account:e.email};h.submitUserInfo(r).then(t=>{console.log(t.data),t.data[0]===0?alert("\u6DFB\u52A0\u6210\u529F!"):alert(t.data[1])})};return(r,t)=>{const m=V,n=x,_=g,f=E;return d(),s(f,{"label-position":"top","label-width":"110px",model:e,style:{"max-width":"300px"},class:"mx-auto"},{default:o(()=>[l(n,{label:"LeetCode\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.leetcode,"onUpdate:modelValue":t[0]||(t[0]=a=>e.leetcode=a),placeholder:"\u8BF7\u8F93\u5165LeetCode\u8D26\u53F7",required:""},null,8,["modelValue"])]),_:1}),l(n,{label:"Github\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.github,"onUpdate:modelValue":t[1]||(t[1]=a=>e.github=a),placeholder:"Github\u7528\u6237\u540D"},{prepend:o(()=>[i("Https://github.com/")]),_:1},8,["modelValue"])]),_:1}),l(n,{label:"\u90AE\u7BB1\u8D26\u53F7"},{default:o(()=>[l(m,{type:"email",modelValue:e.email,"onUpdate:modelValue":t[2]||(t[2]=a=>e.email=a),placeholder:"Email"},null,8,["modelValue"])]),_:1}),l(n,null,{default:o(()=>[l(_,{type:"primary",onClick:u},{default:o(()=>[i("\u63D0\u4EA4\u7ED1\u5B9A")]),_:1})]),_:1})]),_:1},8,["model"])}}},I={__name:"UserView",setup(c){return(e,u)=>(d(),s(U))}};export{I as default};