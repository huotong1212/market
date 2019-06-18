<template>
    <div>
        <!--允许多个工作经验-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="item in projectExperience" :key="item.id" name="item.id">
                <template slot="title" >
                    <i class="header-icon el-icon-arrow-right"></i><p class="tform">{{item.project_name}}</p>
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
                        <el-form-item label="项目名称">
                            <el-input v-model="item.project_name"></el-input>
                        </el-form-item>
                        <el-form-item label="技术使用">
                            <el-input v-model="item.project_skills"></el-input>
                        </el-form-item>
                        <el-form-item label="项目职责">
                            <el-input type="textarea" rows="3" v-model="item.tasks"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        name: "ProjectExperience",
        data:function () {
            return{
                activeNames: ['1'],
                projectExperience:[
                    {
                        "id": 1,
                        "start_time": "2019-01-08T19:48:28",
                        "end_time": "2019-06-17T19:48:28",
                        "project_name": "浦发硅谷银行项目",
                        "project_skills": "JAVA/Angular",
                        "tasks": "1.根据需求，搭建整个签约放款的流程（从放款申请到放款批复），并同时实现前端的界面展示和后台的逻辑处理。\r\n2.负责特殊批复（放款特殊批复和Tranche申请）的功能需求实现，包括前后端的功能实现和数据库表的创建与维护工作。\r\n3.负责统计查询模块的功能设计和实现，确保可以按照需求查询和展示相应的数据。",
                        "resume_id": 1
                    },
                    {
                        "id": 2,
                        "start_time": "2019-01-08T19:48:28",
                        "end_time": "2019-06-17T19:48:28",
                        "project_name": "Google阿尔法狗项目",
                        "project_skills": "JAVA/Angular",
                        "tasks": "1.根据需求，搭建整个签约放款的流程（从放款申请到放款批复），并同时实现前端的界面展示和后台的逻辑处理。\r\n2.负责特殊批复（放款特殊批复和Tranche申请）的功能需求实现，包括前后端的功能实现和数据库表的创建与维护工作。\r\n3.负责统计查询模块的功能设计和实现，确保可以按照需求查询和展示相应的数据。",
                        "resume_id": 1
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
