<template>
    <div>
        <!--允许多个工作经验-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item v-for="item in workExperience" :key="item.id" name="item.id">
                <template slot="title">
                    <span style="width: 90%">
                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{item.company}}</span>
                    </span>
                    <el-button type="text" icon="el-icon-delete" @click="deleteThisExperience(item.id)">删除</el-button>
                </template>

                <!--WorkExperience-->
                <div class="form-box">
                    <el-form ref="item" :rules="rules" :model="item" label-width="80px">
                        <el-form-item label="企业名称" prop="company">
                            <el-input maxlength="20" v-model="item.company"></el-input>
                        </el-form-item>
                        <el-form-item label="时期" >
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" type="date" placeholder="开始时间" v-model="item.start_time"
                                                style="width: 100%;"></el-date-picker>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" placeholder="结束时间" v-model="item.end_time"
                                                style="width: 100%;"></el-date-picker>
                            </el-col>
                            <span v-show="item.error" style="font-size: small;color: #f02d2d">起始日期不可大于结束日期</span>
                        </el-form-item>
                        <el-form-item label="任职部门" prop="department">
                            <el-input maxlength="100" v-model="item.department"></el-input>
                        </el-form-item>
                        <el-form-item label="任职岗位" prop="profession">
                            <el-input maxlength="100" v-model="item.profession"></el-input>
                        </el-form-item>
                        <el-form-item label="岗位职责" prop="duty">
                            <el-input maxlength="100" type="textarea" rows="3" v-model="item.duty"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    import {createWorkExperience, deleteWorkExperience, getAllWorkExperience, updateWorkExperience} from "../api/api";
    import cookie from "../static/cookie";
    import Vue from 'vue'

    export default {
        name: "WorkExperience",
        data: function () {
            return {
                activeNames: ['1'],
                workExperience: [

                ],
                rules: {
                    company: [
                        {max: 20, message: '长度在 20 个字符之内'}
                    ],
                    profession: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                    department: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                    duty: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                },
                error:false,
            }
        },
        methods: {
            handleChange(val) {
                // console.log(this.activeNames)
                // console.log(val);
            },
            getAllWorkExperience() {
                getAllWorkExperience(
                    {
                        resumeId:this.resumeId
                    }
                ).then((response) => {
                    //箭头函数中的this是这个vue对象
                    //console.log('workExperience', response)
                    this.workExperience = response.data
                }).catch(function (error) {

                });
            },
            deleteThisExperience(experienceId) {
                const index = this.workExperience.findIndex(item => item.id === experienceId);
                deleteWorkExperience(
                    experienceId,
                    {}
                ).then((response) => {
                    console.log('deleteWorkExperience', response)
                    this.workExperience.splice(index, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                }).catch(function (error) {

                })
            },
            createWorkExperience(){
                createWorkExperience({
                        resume_id:this.resumeId
                    }
                ).then((response)=>{
                    console.log('create-WorkExperience',response)
                    this.workExperience.push(response.data)
                }).catch(function (error) {
                    // console.log(error)
                })
            },
            saveWorkExperience(){
                // this.$refs.form[0].validate((valid) => {
                //     if(valid && !this.error){
                if(!this.error){
                    updateWorkExperience(this.resumeId,
                        this.workExperience
                    ).then((response)=>{
                        console.log('save-WorkExperience',response)
                    }).catch(function (error) {
                        // console.log(error)
                    })
                }
                // });
            },
            dateChange(id){
                const index = this.workExperience.findIndex(item => item.id === id);
                if(this.workExperience[index].end_time < this.workExperience[index].start_time){
                    Vue.set(this.workExperience[index], 'error', true)
                    this.error = true
                }else {
                    Vue.set(this.workExperience[index], 'error', false)
                    this.error = false
                }
                console.log(index,this.workExperience[index])
            }
        },
        mounted() {
            this.resumeId = cookie.getCookie('resumeId')
            this.getAllWorkExperience()
        }
    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium", "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        font-size: 16px;
    }
</style>
