<template>
    <div>
        <!--允许多个工作经验-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="item in education" :key="item.id" name="item.id">
                <template slot="title" >
                    <i class="header-icon el-icon-arrow-right"></i><p class="tform">{{item.graduate_school}}</p>
                </template>

                <!--Education-->
                <div class="form-box">
                    <el-form ref="item" :model="item" label-width="80px">
                        <el-form-item label="时期">
                            <el-col :span="11">
                                <el-date-picker type="date" placeholder="入学日期" v-model="item.enrollment_date" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-date-picker placeholder="毕业日期" v-model="item.graduate_date" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>
                        <el-form-item label="毕业院校">
                            <el-input v-model="item.graduate_school"></el-input>
                        </el-form-item>
                        <el-form-item label="课程描述">
                            <el-input v-model="item.subjects"></el-input>
                        </el-form-item>
                        <el-form-item label="突出表现">
                            <el-input type="textarea" rows="3" v-model="item.emphasize"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        name: "Education",
        data:function () {
            return{
                activeNames: ['1'],
                education:[
                    {
                        id: 1,
                        enrollment_date: "2014-07-01T18:56:01",
                        graduate_date: "2018-07-01T18:56:01",
                        graduate_school: "苏州科技大学",
                        subjects: "程序设计语言(C语言)、计算机辅助设计、数据库原理与应用、地理信息系统开发与编程、Web程序设计、数据结构。",
                        emphasize: "2018届优秀毕业生",
                        resume_id: 1
                    },
                    {
                        id: 2,
                        enrollment_date: "2014-08-01T18:56:01",
                        graduate_date: "2018-09-01T18:56:01",
                        graduate_school: "苏州科技大学",
                        subjects: "程序设计语言(C语言)、计算机辅助设计、数据库原理与应用、地理信息系统开发与编程、Web程序设计、数据结构。",
                        emphasize: "2018届优秀毕业生",
                        resume_id: 1
                    }
                ]
            }
        },
        methods:{
            handleChange(val) {
                console.log(this.activeNames)
                console.log(val);
            }
        },
    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium","Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size: 16px;
    }
</style>
