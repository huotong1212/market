<template>
    <div>
        <!--允许多个教育背景-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="item in education" :key="item.id" :name="item.graduate_school">
                <template slot="title" >
                    <span style="width: 90%">
                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{item.graduate_school}}</span>
                    </span>
                    <el-button type="text" icon="el-icon-delete" @click="deleteThisEducation(item.id)">删除</el-button>
                </template>

                <!--Education-->
                <div class="form-box">
                    <el-form ref="form" :rules="rules" :model="item" label-width="80px">
                        <el-form-item label="时期" prop="enrollment_date">
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" type="date" placeholder="入学日期" v-model="item.enrollment_date" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)" placeholder="毕业日期" v-model="item.graduate_date" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <span v-show="item.error" style="font-size: small;color: #f02d2d">入学日期不可大于毕业日期</span>
                            <!--                            <el-date-picker-->
<!--                                    v-model="item.dataP"-->
<!--                                    type="daterange"-->
<!--                                    range-separator="至"-->
<!--                                    value-format="yyyy-MM-dd"-->
<!--                                    @change="dateChange(item.id)"-->
<!--                                    start-placeholder="开始日期"-->
<!--                                    end-placeholder="结束日期">-->
<!--                            </el-date-picker>-->
                        </el-form-item>
                        <el-form-item label="毕业院校" prop="graduate_school">
                            <el-input maxlength="20" v-model="item.graduate_school"></el-input>
                        </el-form-item>
                        <el-form-item label="课程描述" prop="subjects">
                            <el-input maxlength="100"  v-model="item.subjects"></el-input>
                        </el-form-item>
                        <el-form-item label="突出表现" prop="emphasize">
                            <el-input maxlength="100" type="textarea" rows="3" v-model="item.emphasize"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>

    </div>
</template>

<script>
    import {createEducation, deleteEducation, getAllEducation, updateEducation} from "../api/api";
    import cookie from "../static/cookie";
    import Vue from 'vue'

    export default {
        name: "Education",
        data:function () {
            return{
                value1:[],
                activeNames: ['1'],
                education:[
                ],
                resumeId:'',
                error:false,
                rules: {
                    graduate_school: [
                        {max: 20, message: '长度在 20 个字符之内'}
                    ],
                    subjects: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                    emphasize: [
                        {max: 100, message: '长度在 100 个字符之内'}
                    ],
                }
            }
        },
        computed:{

        },
        // props:[
        //   'createEdu'
        // ],
        methods:{
            // dateRange(id){
            //     const index = this.education.findIndex(item => item.id === id);
            //     return [this.education[index].enrollment_date,this.education[index].graduate_date]
            // },
            handleChange(val) {
                // console.log(this.activeNames)
                // console.log(val);
            },
            getAllEducation(){
                getAllEducation(
                    this.resumeId
                ).then((response) => {
                    //箭头函数中的this是这个vue对象
                    this.education = response.data
                }).catch(function (error) {
                });
            },
            deleteThisEducation(educationId){
                const index = this.education.findIndex(item => item.id === educationId);
                deleteEducation(
                    educationId,
                    {}
                ).then((response)=>{
                    console.log('deleteEducation',response)
                    this.education.splice(index,1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                }).catch(function (error) {

                })
            },
            createEducation(){
                createEducation({
                    resume_id:this.resumeId
                    }
                ).then((response)=>{
                    console.log('create-Education',response)
                    this.education.push(response.data)
                }).catch(function (error) {
                    // console.log(error)
                })
            },
            saveEducations(){
                // this.$refs.form[0].validate((valid) => {
                //     if(valid && !this.error){
                if(!this.error){
                    updateEducation(this.resumeId,
                            this.education
                        ).then((response)=>{
                            console.log('save-Education',response)
                        }).catch(function (error) {
                            // console.log(error)
                        })
                    }
                // });

            },
            dateChange(id){
                const index = this.education.findIndex(item => item.id === id);
                if(this.education[index].graduate_date < this.education[index].enrollment_date){
                    Vue.set(this.education[index], 'error', true)
                    this.error = true
                }else {
                    Vue.set(this.education[index], 'error', false)
                    this.error = false
                }
                console.log(index,this.education[index])
            }
        },
        // watch:{
        //     createEdu(val){
        //         console.log('createEdu',this.createEdu) //true
        //         console.log('val',val)  //true
        //
        //         if(this.createEdu){
        //             this.createEducation()
        //         }
        //     }
        // },

        created() {
            // this.resumeId = cookie.getCookie('resumeId')
            // this.getAllEducation()
        },
        activated() {
            // this.resumeId = cookie.getCookie('resumeId')
            // this.getAllEducation()
        },
        mounted() {
            this.resumeId = cookie.getCookie('resumeId')
            this.getAllEducation()
        }
    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium","Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size: 16px;
    }
</style>
