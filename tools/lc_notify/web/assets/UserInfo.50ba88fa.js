import{ai as f,E as h,B as i,C as s,D as o,$ as l,X as r,aO as g,aQ as V}from"./index.10b7dc21.js";/* empty css                */import{a as x,E,b as U}from"./el-form-item.e50b5df3.js";const B={__name:"BindForm",setup(c){const e=f({leetcode:"",github:"",email:""}),u=()=>{_()},_=()=>{if(e.leetcode===""){alert("LeetCode\u8D26\u6237\u4E0D\u80FD\u4E3A\u7A7A!");return}const d={lc_account:e.leetcode,git_account:"https://github.com/"+e.github,email_account:e.email};g.submitUserInfo(d).then(t=>{console.log(t.data),t.data[0]===0?alert("\u6DFB\u52A0\u6210\u529F!"):alert(t.data[1])})};return(d,t)=>{const m=h,n=x,p=E,b=U;return i(),s(b,{"label-position":"top","label-width":"110px",model:e,style:{"max-width":"300px"},class:"mx-auto"},{default:o(()=>[l(n,{label:"LeetCode\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.leetcode,"onUpdate:modelValue":t[0]||(t[0]=a=>e.leetcode=a),placeholder:"\u8BF7\u8F93\u5165LeetCode\u8D26\u53F7",required:""},null,8,["modelValue"])]),_:1}),l(n,{label:"Github\u8D26\u53F7"},{default:o(()=>[l(m,{modelValue:e.github,"onUpdate:modelValue":t[1]||(t[1]=a=>e.github=a),placeholder:"Github\u7528\u6237\u540D"},{prepend:o(()=>[r("Https://github.com/")]),_:1},8,["modelValue"])]),_:1}),l(n,{label:"\u90AE\u7BB1\u8D26\u53F7"},{default:o(()=>[l(m,{type:"email",modelValue:e.email,"onUpdate:modelValue":t[2]||(t[2]=a=>e.email=a),placeholder:"Email"},null,8,["modelValue"])]),_:1}),l(n,null,{default:o(()=>[l(p,{type:"primary",onClick:u},{default:o(()=>[r("\u63D0\u4EA4\u7ED1\u5B9A")]),_:1})]),_:1})]),_:1},8,["model"])}}},L={__name:"UserInfo",setup(c){return(e,u)=>(i(),s(V,null,{bind_form:o(()=>[l(B)]),_:1}))}};export{L as default};