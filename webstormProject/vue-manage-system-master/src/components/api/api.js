import axios from 'axios';


let host = 'http://shop.projectsedu.com';
let localhost = 'http://127.0.0.1:8000';


//-----------------User(用户)---------------------

//登录
export const login = params => {
    return axios.post(`${localhost}/login/`, params)
}

//获取当前用户信息
export const getUser = () => {
    return axios.get(`${localhost}/user/1`)
}

//用户注册
export const register = params => {
    return axios.post(`${localhost}/user/`, params)
}

//修改用户信息
export const updateUserInfo = params => { return axios.patch(`${localhost}/user/1/`, params) }

//-----------------VerifyCode(验证码)---------------------

//短信验证码，获取
export const getSMSCode = phoneNum => { return axios.post(`${localhost}/sms/`, phoneNum) }

//邮箱验证码，获取
export const getEmailCode = email => { return axios.post(`${localhost}/email/`, email) }


//-----------------UserResume(用户简历)---------------------

//获取所有简历(带参数的get)【params是筛选，排序的数据】
export const getAllUserResume = params => {
    return axios.get(`${localhost}/userResume/`, {params:params})
}

//获取单个简历(带参数的get)
export const getUserResume = resumeId => {
    return axios.get(`${localhost}/userResume/${resumeId}/`)
}

//创建简历(带参数的post)
export const createUserResume = params => {
    return axios.post(`${localhost}/userResume/`, params)
}

//更新简历(带参数的patch)
export const updateUserResume = (resumeId,params) => {
    return axios.patch(`${localhost}/userResume/${resumeId}/`, params)
}

//删除简历(带参数的patch) [包括单个删除，或者批量删除]
export const deleteUserResume = (resumeId,params) => {
    return axios.delete(`${localhost}/userResume/${resumeId}/`, {data:params})
}

//-----------------SkillCategory(用户简历)---------------------
//获取所有技能的一级分类(带参数的get)【params是筛选，排序的数据】
export const getSkillCategory = params => {
    return axios.get(`${localhost}/userResume/`, {params:params})
}

//-----------------Expectation(期望职业)---------------------

// 获取期望职业
export const getExpectation = resumeId => {
    return axios.get(`${localhost}/expectation/${resumeId}`)
}

//创建期望职业(带参数的post)
export const createExpectation = params => {
    return axios.post(`${localhost}/expectation/`, params)
}

//更新期望职业(带参数的patch)
export const updateExpectation = (resumeId,params) => {
    return axios.patch(`${localhost}/expectation/${resumeId}/`, params)
}

//删除期望职业(带参数的patch) [包括单个删除，或者批量删除]
export const deleteExpectation = (resumeId,params) => {
    return axios.delete(`${localhost}/expectation/${resumeId}/`, params)
}

//-----------------Education(教育背景)---------------------

// 获取教育背景【单个】
export const getEducation = educationId => {
    return axios.get(`${localhost}/education/${educationId}`)
}

// 获取教育背景【多个】
export const getAllEducation = (params) => {
    return axios.get(`${localhost}/education/`,{params:params})
}

//创建教育背景(带参数的post)
export const createEducation = params => {
    return axios.post(`${localhost}/education/`, params)
}

//更新教育背景(带参数的patch)
export const updateEducation = (resumeId,params) => {
    return axios.patch(`${localhost}/education/${resumeId}/`, params)
}

//删除教育背景(带参数的patch) [包括单个删除，或者批量删除]
export const deleteEducation = (educationId,params) => {
    return axios.delete(`${localhost}/education/${educationId}/`, params)
}

//-----------------WorkExperience(工作经验)---------------------

// 获取工作经验【单个】
export const getWorkExperience = WorkExperienceId => {
    return axios.get(`${localhost}/workExperience/${WorkExperienceId}`)
}

// 获取工作经验【多个】
export const getAllWorkExperience = (params) => {
    return axios.get(`${localhost}/workExperience/`,{params:params})
}

//创建工作经验(带参数的post)
export const createWorkExperience = params => {
    return axios.post(`${localhost}/workExperience/`, params)
}

//更新工作经验(带参数的patch)
export const updateWorkExperience = (resumeId,params) => {
    return axios.patch(`${localhost}/workExperience/${resumeId}/`, params)
}

//删除工作经验(带参数的patch) [包括单个删除，或者批量删除]
export const deleteWorkExperience = (WorkExperienceId,params) => {
    return axios.delete(`${localhost}/workExperience/${WorkExperienceId}/`, params)
}

//-----------------ProjectExperience(项目经验)---------------------

// 获取项目经验【单个】
export const getProjectExperience = ProjectExperienceId => {
    return axios.get(`${localhost}/projectExperience/${ProjectExperienceId}`)
}

// 获取项目经验【多个】
export const getAllProjectExperience = (params) => {
    return axios.get(`${localhost}/projectExperience/`,{params:params})
}

//创建项目经验(带参数的post)
export const createProjectExperience = params => {
    return axios.post(`${localhost}/projectExperience/`, params)
}

//更新项目经验(带参数的patch)
export const updateProjectExperience = (resumeId,params) => {
    return axios.patch(`${localhost}/projectExperience/${resumeId}/`, params)
}

//删除项目经验(带参数的patch) [包括单个删除，或者批量删除]
export const deleteProjectExperience = (ProjectExperienceId,params) => {
    return axios.delete(`${localhost}/projectExperience/${ProjectExperienceId}/`, params)
}

//-----------------Skills(技能特长)---------------------

// 获取技能特长【单个】
export const getSkills = SkillsId => {
    return axios.get(`${localhost}/skills/${SkillsId}`)
}

// 获取技能特长【多个】
export const getAllSkills = (params) => {
    return axios.get(`${localhost}/skills/`,{params:params})
}

//创建技能特长(带参数的post)
export const createSkills = params => {
    return axios.post(`${localhost}/skills/`, params)
}

//更新技能特长(带参数的patch)
export const updateSkills = (SkillsId,params) => {
    return axios.patch(`${localhost}/skills/${SkillsId}/`, params)
}

//删除技能特长(带参数的patch) [包括单个删除，或者批量删除]
export const deleteSkills = (SkillsId,params) => {
    return axios.delete(`${localhost}/skills/${SkillsId}/`, {data:params})
}

//-----------------SelfAppraise(自我评价)---------------------

// 获取自我评价【单个】
export const getSelfAppraise = resumeId => {
    return axios.get(`${localhost}/selfAppraise/${resumeId}`)
}

// 获取自我评价【多个】
export const getAllSelfAppraise = (params) => {
    return axios.get(`${localhost}/selfAppraise/`,{params:params})
}

//创建自我评价(带参数的post)
export const createSelfAppraise = params => {
    return axios.post(`${localhost}/selfAppraise/`, params)
}

//更新自我评价(带参数的patch)
export const updateSelfAppraise = (resumeId,params) => {
    return axios.patch(`${localhost}/selfAppraise/${resumeId}/`, params)
}

//删除自我评价(带参数的patch) [包括单个删除，或者批量删除]
export const deleteSelfAppraise = (SelfAppraiseId,params) => {
    return axios.delete(`${localhost}/selfAppraise/${SelfAppraiseId}/`, params)
}
