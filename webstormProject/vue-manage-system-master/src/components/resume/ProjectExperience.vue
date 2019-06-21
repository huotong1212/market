<template>
    <div>
        <!--允许多个工作经验-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="item in projectExperience" :key="item.id" name="item.id">
                <template slot="title" >
                    <span style="width: 90%">
                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{item.project_name}}</span>
                     </span>
                    <el-button type="text" icon="el-icon-delete" @click="deleteThisProject(item.id)">删除</el-button>
                </template>

                <!--Education-->
                <div class="form-box">
                    <el-form ref="item" :rules="rules" :model="item" label-width="80px">
                        <el-form-item label="时期">
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" type="date" placeholder="开始时间" v-model="item.start_time" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" placeholder="结束时间" v-model="item.end_time" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <span v-show="item.error" style="font-size: small;color: #f02d2d">起始日期不可大于结束日期</span>
                        </el-form-item>
                        <el-form-item label="项目名称" prop="project_name">
                            <el-input maxlength="30" v-model="item.project_name"></el-input>
                        </el-form-item>
                        <el-form-item label="技术使用" prop="project_skills">
                            <el-input maxlength="100" v-model="item.project_skills"></el-input>
                        </el-form-item>
                        <el-form-item label="项目职责" prop="tasks">
                            <el-input maxlength="1000" type="textarea" rows="3" v-model="item.tasks"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    import {
        createProjectExperience,
        deleteProjectExperience,
        getAllProjectExperience,
        updateProjectExperience
    } from "../api/api";
    import Vue from 'vue'
    import cookie from "../static/cookie";

    export default {
        name: "ProjectExperience",
        data:function () {
            return{
                activeNames: ['1'],
                resumeId:'',
                projectExperience:[

                ],
                rules: {
                    project_name: [
                        {max: 30, message: '长度在 30 个字符之内'}
                    ],
                    project_skills: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                    tasks: [
                        {max: 1000, message: '长度在 1000 个字符之内'}
                    ],
                },
                error:false,
            }
        },
        methods:{
            handleChange(val) {
                // console.log(this.activeNames)
                // console.log(val);
            },
            getAllProjectExperience() {
                getAllProjectExperience(
                    this.resumeId
                ).then((response) => {
                    //箭头函数中的this是这个vue对象
                    //console.log('getAllProjectExperience', response)
                    this.projectExperience = response.data
                }).catch(function (error) {

                });
            },

            saveProjectExperience(){
                // this.$refs.form[0].validate((valid) => {
                //     if(valid && !this.error){
                if(!this.error){
                    updateProjectExperience(this.resumeId,
                        this.projectExperience
                    ).then((response)=>{
                        console.log('save-WorkExperience',response)
                    }).catch(function (error) {
                        // console.log(error)
                    })
                }
                // });
            },

            deleteThisProject(projectId) {
                const index = this.projectExperience.findIndex(item => item.id === projectId);
                deleteProjectExperience(
                    projectId,
                    {}
                ).then((response) => {
                    console.log('deleteThisProject', response)
                    this.projectExperience.splice(index, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                }).catch(function (error) {

                })
            },
            dateChange(id){
                const index = this.projectExperience.findIndex(item => item.id === id);
                if(this.projectExperience[index].end_time < this.projectExperience[index].start_time){
                    Vue.set(this.projectExperience[index], 'error', true)
                    this.error = true
                }else {
                    Vue.set(this.projectExperience[index], 'error', false)
                    this.error = false
                }
                console.log(index,this.projectExperience[index])
            },
            createProjectExperience(){
                createProjectExperience({
                        resume_id:this.resumeId
                    }
                ).then((response)=>{
                    console.log('createProjectExperience',response)
                    this.projectExperience.push(response.data)
                }).catch(function (error) {
                    // console.log(error)
                })
            },
        },
        mounted() {
            this.resumeId = cookie.getCookie('resumeId')
            this.getAllProjectExperience()
        }
    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium","Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size: 16px;
    }
</style>
