import{r as l,j as e}from"./@radix-DeK6qiuw.js";import{u as m,S as I,C as x,P as f,W as B,L as M}from"./ProviderRadio-8f43sPD4.js";import{p as C,s as A,c as k}from"./persist-GjC8PZoC.js";import{I as b}from"./Infobox-Cx4xGoXR.js";import{W as v,H as g,B as y,S as N}from"./WizardFooter-dgmizSJC.js";import{t as z}from"./zod-BwEbpOxH.js";import{f as u,aF as F,S as P,r as Z,z as _}from"./index-CCOPpudF.js";import{u as T,F as L,b as W}from"./index.esm-Dy6Z9Ung.js";import{R as V,a as H,E as O,C as $}from"./Partials-03iZf8-N.js";import{a as G,d as Q}from"./persist-Coz7ZWvz.js";import{S as Y}from"./link-external-b9AXw_sW.js";import{S as q}from"./logs-WMSM52RF.js";import{C as j}from"./CodeSnippet-JzR8CEtw.js";import{N as w}from"./NumberBox-Dtp3J6g5.js";import{s as E}from"./index-CEV4Cvaf.js";import{a as D}from"./@tanstack-DT5WLu9C.js";import{b as J}from"./@react-router-B3Z5rLr2.js";import{C as h}from"./ProviderIcon-Bki2aw8w.js";import"./Tick-BlMoIlJT.js";import"./check-DloQpStc.js";import"./@reactflow-CK0KJUen.js";import"./package-C6uypY4h.js";import"./ComponentBadge-D_g62Wv8.js";import"./stack-detail-query-OPEW-cDJ.js";import"./layout-BtHBmE4w.js";import"./rocket-DjT2cDvG.js";import"./sharedSchema-CQb14VSr.js";import"./copy-C8XQA2Ug.js";import"./url-CkvKAnwF.js";import"./gcp-CFtm4BA7.js";const R=l.createContext(null);function K({children:r}){const{setCurrentStep:t}=m(),[i,s]=l.useState({}),[o,c]=l.useState("");return l.useEffect(()=>{const{success:a,data:n}=C();if(a){t(3),s({location:n.location,provider:n.provider,stackName:n.stackName}),c(n.timestamp);return}t(1)},[C]),e.jsx(R.Provider,{value:{data:i,setData:s,timestamp:o,setTimestamp:c},children:r})}function d(){const r=l.useContext(R);if(r===null)throw new Error("useCreateTerraformContext must be used within an CreateTerraformContext");return r}function U(){const{setData:r,data:t,setTimestamp:i}=d(),{setCurrentStep:s}=m(),o=T({resolver:z(G,{async:!0}),defaultValues:{region:t.location||"",stackName:t.stackName||""}});function c(a){const n=new Date().toISOString().slice(0,-1);A({location:a.region,provider:t.provider||"aws",stackName:a.stackName,timestamp:n}),i(n),r(p=>({...p,location:a.region,stackName:a.stackName})),s(p=>p+1)}return e.jsx(L,{...o,children:e.jsxs(v,{children:[e.jsx(g,{children:"Review Stack Configuration"}),e.jsx(y,{children:e.jsxs("div",{className:"space-y-5",children:[e.jsxs(b,{className:"text-text-sm",children:[e.jsx("p",{className:"font-semibold",children:"Important"}),e.jsx("p",{children:"This will create new resources in your account. Ensure you have the necessary permissions and are aware of any potential costs."})]}),e.jsxs("form",{id:"configuration-form",onSubmit:o.handleSubmit(c),className:"space-y-5",children:[e.jsx(V,{provider:t.provider||"aws"}),e.jsx(I,{})]}),e.jsx(H,{provider:t.provider||"aws"}),e.jsx(O,{provider:t.provider||"aws"})]})}),e.jsx(N,{children:e.jsx(X,{})})]})})}function X(){const{formState:{isSubmitting:r}}=W();return e.jsx(u,{disabled:r,form:"configuration-form",size:"md",children:"Next"})}function ee(){return e.jsxs("div",{className:"space-y-5",children:[e.jsx("div",{className:"space-y-1",children:e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(w,{children:"3"}),e.jsx("span",{className:"text-text-lg font-semibold",children:"Run the following commands"})]})}),e.jsxs("div",{children:[e.jsx("p",{className:"mb-1 text-text-sm text-theme-text-secondary",children:"Initialize the Terraform configuration."}),e.jsx(j,{code:"terraform init --upgrade"})]}),e.jsxs("div",{children:[e.jsx("p",{className:"mb-1 text-text-sm text-theme-text-secondary",children:"Run terraform apply to deploy the ZenML stack to Azure."}),e.jsx(j,{code:"terraform apply"})]})]})}function re(){const{data:r,timestamp:t}=d(),{setCurrentStep:i}=m(),s=D({...E.stackDeploymentStack({provider:r.provider,stack_name:r.stackName,date_start:t,terraform:!0}),refetchInterval:5e3,throwOnError:!0});return l.useEffect(()=>{s.data&&(k(),i(o=>o+1))},[s.data]),{fullstackDeployment:s,data:r}}function te(){const{fullstackDeployment:r,data:t}=re();return r.isError?e.jsx("p",{children:"Error fetching Terraform Command"}):r.isPending?e.jsx(P,{className:"h-[200px] w-full"}):e.jsx(ae,{provider:t.provider||"aws",stackName:t.stackName||""})}function se(){return e.jsxs("section",{className:"space-y-5 border-t border-theme-border-moderate pt-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(F,{className:"h-5 w-5 fill-primary-400"}),"Waiting for your Terraform script to finish..."]}),e.jsx("p",{className:"text-theme-text-secondary",children:"We are detecting whether your Terraform script ran through successfully. Once the terraform script has finished successfully, come back to check your brand new stack and components ready."})]}),e.jsx(te,{})]})}function ae({stackName:r,provider:t}){return e.jsxs("div",{className:"relative overflow-hidden rounded-md",children:[e.jsx("div",{className:"absolute z-50 h-full w-full bg-neutral-50/50"}),e.jsx($,{type:t,componentProps:{isLoading:!0,isSuccess:!1,stackName:r}})]})}function oe(){return e.jsxs(v,{children:[e.jsx(g,{children:"Deploy ZenML Stack"}),e.jsx(y,{children:e.jsxs("section",{className:"space-y-5",children:[e.jsx(ne,{}),e.jsx(de,{}),e.jsx(me,{}),e.jsx(ee,{}),e.jsx(se,{})]})}),e.jsxs(N,{displayCancel:!1,children:[e.jsx(pe,{}),e.jsx(ie,{})]})]})}function ie(){return e.jsx(u,{disabled:!0,size:"md",children:"Next"})}function ne(){return e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(q,{className:"h-5 w-5 fill-primary-400"}),"Configuration"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"Follow the steps to deploy your Stack."})]})}function ce(r){switch(r){case"aws":return"https://aws.amazon.com/cli/";case"azure":return"https://learn.microsoft.com/en-us/cli/azure/";case"gcp":return"https://cloud.google.com/sdk/gcloud"}}function le(r){switch(r){case"aws":return"AWS";case"gcp":return"gcloud";case"azure":return"Azure"}}function de(){const{data:r}=d();return e.jsx("div",{className:"space-y-5",children:e.jsxs("div",{className:"space-y-1",children:[e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(w,{children:"1"}),e.jsxs("span",{className:"text-text-lg font-semibold",children:["Login locally with the ",le(r.provider||"aws")," CLI"]})]}),e.jsx("p",{className:"text-theme-text-secondary",children:"Make sure you are logged in locally with an account with appropriate permissions."}),e.jsx(u,{asChild:!0,className:"w-fit gap-1",intent:"secondary",emphasis:"subtle",size:"md",children:e.jsxs("a",{rel:"noopener noreferrer",target:"_blank",href:ce(r.provider||"aws"),children:[e.jsx("span",{children:"Learn More"}),e.jsx(Y,{className:"h-5 w-5 shrink-0 fill-primary-900"})]})})]})})}function me(){const{data:r}=d();return e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(w,{children:"2"}),e.jsx("span",{className:"text-text-lg font-semibold",children:"Create a file with the following configuration"})]}),e.jsxs("p",{className:"text-theme-text-secondary",children:["Create a file named ",e.jsx("code",{className:"font-mono text-primary-400",children:"main.tf"})," in the Cloud Shell and copy and paste the Terraform configuration below into it."]})]}),r.provider==="gcp"&&e.jsxs(b,{intent:"warning",children:["Please replace ",e.jsx("code",{className:"font-mono text-primary-400",children:"project_id"})," in the following Terraform script with your own one."]}),e.jsx(ue,{})]})}function ue(){const{data:r}=d(),t=D({...E.stackDeploymentConfig({provider:r.provider||"aws",terraform:!0,stack_name:r.stackName,location:r.location}),enabled:!!r.stackName});return t.isError?null:t.isPending?e.jsx(P,{className:"h-[200px] w-full"}):e.jsx(j,{fullWidth:!0,highlightCode:!0,codeClasses:"whitespace-pre-wrap word-break-all",wrap:!0,code:t.data.configuration||""})}function pe(){const r=J();function t(){k(),r(Z.stacks.create.index)}return e.jsx(u,{onClick:()=>t(),intent:"secondary",size:"md",children:"Cancel"})}const xe=_.object({provider:Q});function fe(){const{setData:r,data:t}=d(),{setCurrentStep:i}=m(),s=T({resolver:z(xe),defaultValues:{provider:t.provider||void 0}});function o(c){r(a=>({...a,provider:c.provider})),i(a=>a+1)}return e.jsx(L,{...s,children:e.jsxs(v,{children:[e.jsx(g,{children:"New Cloud infrastructure"}),e.jsx(y,{children:e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsx("p",{className:"text-text-lg font-semibold",children:"Select a Cloud Provider"}),e.jsx("p",{className:"text-theme-text-secondary",children:"Select the cloud provider where your want to create your infrastructure. You will be able to remove the ZenML stack at any time."})]}),e.jsxs("form",{id:"provider-form",onSubmit:s.handleSubmit(o),className:"grid grid-cols-1 gap-3 xl:grid-cols-3",children:[e.jsx(x,{id:"aws-provider",...s.register("provider"),value:"aws",children:e.jsx(f,{icon:e.jsx(h,{provider:"aws",className:"h-6 w-6 shrink-0"}),title:"AWS",subtitle:"Connect your existing S3, ECR, and Sagemaker components to ZenML"})}),e.jsx(x,{id:"gcp-provider",...s.register("provider"),value:"gcp",children:e.jsx(f,{icon:e.jsx(h,{provider:"gcp",className:"h-6 w-6 shrink-0"}),title:"GCP",subtitle:"Link your GCS, Artifact Registry, and Vertex AI components to ZenML"})}),e.jsx(x,{id:"azure-provider",...s.register("provider"),value:"azure",children:e.jsx(f,{icon:e.jsx(h,{provider:"azure",className:"h-6 w-6 shrink-0"}),title:"Azure",subtitle:"Integrate ZenML with your Blob Storage, Container Registry, and Azure ML"})})]})]})}),e.jsx(N,{children:e.jsx(he,{})})]})})}function he(){const{formState:{isValid:r}}=W();return e.jsx(u,{form:"provider-form",disabled:!r,size:"md",children:"Next"})}function je(){const{currentStep:r}=m();if(r===1)return e.jsx(fe,{});if(r===2)return e.jsx(U,{});if(r===3)return e.jsx(oe,{})}const S=["Infrastructure Type","Cloud Provider","Review Configuration","Deploy Stack"];function Ye(){return e.jsx(B,{maxSteps:S.length,initialStep:0,children:e.jsx(K,{children:e.jsxs("section",{className:"layout-container flex flex-col gap-5 py-5 xl:flex-row",children:[e.jsx(M,{entries:S}),e.jsx("div",{className:"w-full overflow-y-hidden",children:e.jsx(je,{})})]})})})}export{Ye as default};
