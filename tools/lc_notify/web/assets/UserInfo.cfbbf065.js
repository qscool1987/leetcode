import{ak as b,C as s,D as i,E as o,$ as l,X as r,aG as h,aN as g}from"./index.9fe3a870.js";/* empty css                */import{E as V,c as x,a as E,d as U}from"./el-form-item.295a71ab.js";const C={__name:"BindForm",setup(c){const e=b({leetcode:"",github:"",email:""}),u=()=>{p()},p=()=>{if(e.leetcode===""){alert("LeetCode\u8D26\u6237\u4E0D\u80FD\u4E3A\u7A7A!");return}const d={lc_account:e.leetcode,git_account:"https://github.com/"+e.github,email_account:e.email};h.submitUserInfo(d).then(t=>{console.log(t.data),t.data[0]===0?alert("\u6DFB\u52A0\u6210\u529F!"):alert(t.data[1])})};return(d,t)=>{const m=V,n=x,_=E,f=U;return s(),i(f,{"label-position":"top","label-width":"110px",model:e,style:{"max-width":"300px"},class:"mx-auto"},{default:o(()=>[l(n,{label:"LeetCode\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.leetcode,"onUpdate:modelValue":t[0]||(t[0]=a=>e.leetcode=a),placeholder:"\u8BF7\u8F93\u5165LeetCode\u8D26\u53F7",required:""},null,8,["modelValue"])]),_:1}),l(n,{label:"Github\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.github,"onUpdate:modelValue":t[1]||(t[1]=a=>e.github=a),placeholder:"Github\u7528\u6237\u540D"},{prepend:o(()=>[r("Https://github.com/")]),_:1},8,["modelValue"])]),_:1}),l(n,{label:"\u90AE\u7BB1\u8D26\u53F7"},{default:o(()=>[l(m,{type:"email",modelValue:e.email,"onUpdate:modelValue":t[2]||(t[2]=a=>e.email=a),placeholder:"Email"},null,8,["modelValue"])]),_:1}),l(n,null,{default:o(()=>[l(_,{type:"primary",onClick:u},{default:o(()=>[r("\u63D0\u4EA4\u7ED1\u5B9A")]),_:1})]),_:1})]),_:1},8,["model"])}}},y={__name:"UserInfo",setup(c){return(e,u)=>(s(),i(g,null,{"bind-form":o(()=>[l(C)]),_:1}))}};export{y as default};
