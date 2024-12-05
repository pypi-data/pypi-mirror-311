import{j as e}from"./@radix-DeK6qiuw.js";import{B as o,aB as n}from"./index-CCOPpudF.js";import{I as r}from"./Infobox-Cx4xGoXR.js";import{H as a}from"./Helpbox-oYSGpLqd.js";import{V as s,g as c}from"./Commands-DL2kwkRd.js";import"./@tanstack-DT5WLu9C.js";import"./@react-router-B3Z5rLr2.js";import"./@reactflow-CK0KJUen.js";import"./help-Cc9bBIJH.js";import"./CodeSnippet-JzR8CEtw.js";import"./copy-C8XQA2Ug.js";const l=[{command:"zenml code-repository register <NAME> --type=<CODE_REPOSITORY_TYPE] [--CODE_REPOSITORY_OPTIONS]",description:"Register a code repository"},{command:"zenml code-repository register <NAME> --type=custom --source=<CODE_REPOSITORY_SOURCE> [--CODE_REPOSITORY_OPTIONS]",description:"Use a custom repository "},{command:"zenml code-repository list",description:"List your registered code repositories"},{command:"zenml code-repository delete <REPOSITORY_NAME_OR_ID>",description:"Delete a code repository that you have previously registered"}],d="/assets/repos-video-D8kpu60k.svg";function m(){return e.jsx(r,{children:e.jsxs("div",{className:"flex w-full flex-wrap items-center gap-x-2 gap-y-0.5 text-text-md",children:[e.jsx("p",{className:"font-semibold",children:"We are creating a new Repositories experience"}),e.jsx("p",{children:"In the meanwhile you can use the CLI to add and manage your repos."})]})})}function p(){const t="https://zenml.portal.trainn.co/share/koVfVubiXfXLXtVcDAqPyg/embed?autoplay=false";return e.jsxs(o,{className:"flex flex-col-reverse items-stretch overflow-hidden md:flex-row",children:[e.jsxs("div",{className:"w-full p-7 md:w-2/3",children:[e.jsx("h2",{className:"text-display-xs font-semibold",children:"Learn More about Repositories"}),e.jsx("p",{className:"mt-2 text-text-lg text-theme-text-secondary",children:"Get started with ZenML Repositories for streamlined pipeline versioning and faster Docker builds."}),e.jsx(s,{videoLink:t,buttonText:"Watch the Starter Guide (2 min)"})]}),e.jsx("div",{className:"flex w-full items-center justify-center bg-primary-50 lg:w-1/3",children:e.jsx(s,{fallbackImage:e.jsx("img",{src:d,alt:"Purple squares with text indicating a starter guide for secrets",className:"h-full w-full"}),videoLink:t,isButton:!1})})]})}function x(){return e.jsxs("section",{className:"space-y-5 pl-8 pr-5",children:[e.jsx(r,{className:"text-text-md",intent:"neutral",children:"Code repositories enable ZenML to keep track of the code version that you use for your pipeline runs. Additionally, running a pipeline which is tracked in a registered code repository can decrease the time it takes Docker to build images for containerized stack components."}),l.map((t,i)=>e.jsx(e.Fragment,{children:c(t)},i)),e.jsx(a,{text:"Check all the commands and find more about Repositories in our Docs",link:"https://docs.zenml.io/how-to/setting-up-a-project-repository/connect-your-git-repository"})]})}function k(){return e.jsxs(o,{className:"space-y-4 p-5",children:[e.jsx("h1",{className:"text-text-xl font-semibold",children:"Repositories"}),e.jsx(m,{}),e.jsx(p,{}),e.jsxs("div",{className:"flex items-center gap-2",children:[e.jsx(n,{}),"Administering your Code Repositories"]}),e.jsx(x,{})]})}export{k as default};
