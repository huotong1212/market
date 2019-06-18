<template>
    <div>
        <!--允许多个工作经验-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="item in workExperience" :key="item.id" name="item.id">
                <template slot="title" >
                    <i class="header-icon el-icon-arrow-right"></i><p class="tform">{{item.company}}</p>
                </template>

                <!--Education-->
                <div class="form-box">
                    <el-form ref="item" :model="item" label-width="80px">
                        <el-form-item label="时期">
                            <el-col :span="11">
                                <el-date-picker type="date" placeholder="开始时间" v-model="item.start_time" style="width: 100%;"></el-date-picker>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-date-picker placeholder="结束时间" v-model="item.end_time" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>
                        <el-form-item label="任职部门">
                            <el-input v-model="item.department"></el-input>
                        </el-form-item>
                        <el-form-item label="任职岗位">
                            <el-input v-model="item.profession"></el-input>
                        </el-form-item>
                        <el-form-item label="岗位职责">
                            <el-input type="textarea" rows="3" v-model="item.duty"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        name: "WorkExperience",
        data:function () {
            return{
                activeNames: ['1'],
                workExperience:[
                    {
                        "id": 1,
                        "start_time": "2019-06-17T19:37:24",
                        "end_time": "2019-06-17T19:37:24",
                        "company": "上海安硕",
                        "profession": "JAVA开发工程师",
                        "department": "CDC集中开发中心",
                        "duty": "负责银行授信系统部分后台功能的实现和前端界面的开发，包括放款业务的风险探测，前沿检查校验，授信业务流程的处理等",
                        "resume_id": 1
                    },
                    {
                        "id": 2,
                        "start_time": "2019-06-17T19:37:24",
                        "end_time": "2019-06-17T19:37:24",
                        "company": "Google",
                        "profession": "JAVA开发工程师",
                        "department": "硅谷研究中心",
                        "duty": "负责AI，自动驾驶研究",
                        "resume_id": 1
                    },
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
