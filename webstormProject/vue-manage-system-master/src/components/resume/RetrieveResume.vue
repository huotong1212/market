<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>
                <el-breadcrumb-item>创建简历</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">

            <!--基本信息-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">基本信息</span>
                    <!--                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>-->
                </div>

                <!--UserResume表单-->
                <div class="form-box align-center">
                    <el-form ref="form" :model="userResume" label-width="80px">
                        <el-form-item label="姓名">
                            <el-input v-model="userResume.username"></el-input>
                        </el-form-item>
                        <el-form-item label="性别">
                            <el-radio-group v-model="userResume.gender">
                                <el-radio label="male">男</el-radio>
                                <el-radio label="female">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="出身日期">
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" type="date" placeholder="选择日期"
                                                v-model="userResume.birthday" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>

                        <el-form-item label="邮箱">
                            <el-input v-model="userResume.email"></el-input>
                        </el-form-item>

                        <el-form-item label="手机号">
                            <el-input v-model="userResume.mobile"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>

            <!--求职意向-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">求职意向</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--Expectation-->
                <div class="form-box align-center">
                    <el-form ref="form" :model="form" label-width="80px">
                        <el-form-item label="岗位">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>
                        <el-form-item label="城市">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>
                        <!--                        <el-form-item label="到岗时间">-->
                        <!--                            <el-input v-model="form.name"></el-input>-->
                        <!--                        </el-form-item>-->
                        <el-form-item label="到岗时间">
                            <el-select v-model="form.region" placeholder="请选择">
                                <el-option key="1" label="一个月内到岗" value="一个月内到岗"></el-option>
                                <el-option key="2" label="两个月内到岗" value="两个月内到岗"></el-option>
                                <el-option key="3" label="一周内到岗" value="一周内到岗"></el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="薪资范围">
                            <el-col :span="10"> 最低（K）：
                                <el-input-number v-model="form.date" controls-position="right" @change="handleChange"
                                                 :min="1" :max="10">

                                </el-input-number>
                            </el-col>
                            <el-col class="line" :span="1">-</el-col>
                            <el-col :span="11"> 最高（K）：
                                <el-input-number v-model="form.date" controls-position="right" @change="handleChange"
                                                 :min="1" :max="10">
                                </el-input-number>

                            </el-col>
                        </el-form-item>

                    </el-form>
                </div>
            </el-card>

            <!--教育背景-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">教育背景</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--允许多个教育背景-->
                <Education></Education>
            </el-card>

            <!--工作经验-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">工作经验</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--允许多个工作经验-->
                <WorkExperience></WorkExperience>
            </el-card>

            <!--项目经验-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">项目经验</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--允许多个项目经验-->
                <ProjectExperience></ProjectExperience>
            </el-card>

            <!--技能特长-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">技能特长</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--允许多个技能特长-->
                <Skills></Skills>
            </el-card>

            <!--自我评价-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">自我评价</span>
                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                </div>

                <!--自我评价只有一个-->
                <el-input
                        type="textarea"
                        :autosize="{ minRows: 2, maxRows: 4}"
                        placeholder="请输入内容"
                        maxlength="200"
                        v-model="textarea">
                </el-input>
            </el-card>

            <!-- 编辑弹出框 -->
            <el-dialog title="创建简历" :visible.sync="editVisible" width="30%">
                <el-form ref="form" :model="form" label-width="80px">
                    <!--                    <el-form-item label="日期">-->
                    <!--                        <el-date-picker type="date" placeholder="选择日期" v-model="form.date" value-format="yyyy-MM-dd" style="width: 100%;"></el-date-picker>-->
                    <!--                    </el-form-item>-->
                    <el-form-item label="简历名称" placeholder="请输入简历名称">
                        <el-input v-model="userResume.name"></el-input>
                    </el-form-item>
                    <el-form-item label="语言">
                        <el-select v-model="userResume.language" placeholder="请选择语言类型">
                            <el-option label="中文" value="0"></el-option>
                            <el-option label="英语" value="1"></el-option>
                            <el-option label="日语" value="2"></el-option>
                        </el-select>
                    </el-form-item>

                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
            </el-dialog>

            <!--UserResume表单-->
            <div v-show="false" class="form-box align-center">
                <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item label="表单名称">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="选择器">
                        <el-select v-model="form.region" placeholder="请选择">
                            <el-option key="bbk" label="步步高" value="bbk"></el-option>
                            <el-option key="xtc" label="小天才" value="xtc"></el-option>
                            <el-option key="imoo" label="imoo" value="imoo"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="日期时间">
                        <el-col :span="11">
                            <el-date-picker type="date" placeholder="选择日期" v-model="form.date1"
                                            style="width: 100%;"></el-date-picker>
                        </el-col>
                        <el-col class="line" :span="2">-</el-col>
                        <el-col :span="11">
                            <el-time-picker placeholder="选择时间" v-model="form.date2"
                                            style="width: 100%;"></el-time-picker>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="城市级联">
                        <el-cascader :options="options" v-model="form.options"></el-cascader>
                    </el-form-item>
                    <el-form-item label="选择开关">
                        <el-switch v-model="form.delivery"></el-switch>
                    </el-form-item>
                    <el-form-item label="多选框">
                        <el-checkbox-group v-model="form.type">
                            <el-checkbox label="步步高" name="type"></el-checkbox>
                            <el-checkbox label="小天才" name="type"></el-checkbox>
                            <el-checkbox label="imoo" name="type"></el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="单选框">
                        <el-radio-group v-model="form.resource">
                            <el-radio label="步步高"></el-radio>
                            <el-radio label="小天才"></el-radio>
                            <el-radio label="imoo"></el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="文本框">
                        <el-input type="textarea" rows="5" v-model="form.desc"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">表单提交</el-button>
                        <el-button>取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

    </div>
</template>

<script>
    import Education from "./Education";
    import WorkExperience from "./WorkExperience";
    import ProjectExperience from "./ProjectExperience";
    import Skills from "./Skills";
    import SelfAppraise from "./SelfAppraise";
    import customValidate from "../utils/customValidate";
    import cookie from "../static/cookie";

    export default {
        name: 'createResume',
        data: function () {
            return {
                resumeId: '',
                editVisible: false,
                textarea: '',
                options: [
                    {
                        value: 'guangdong',
                        label: '广东省',
                        children: [
                            {
                                value: 'guangzhou',
                                label: '广州市',
                                children: [
                                    {
                                        value: 'tianhe',
                                        label: '天河区'
                                    },
                                    {
                                        value: 'haizhu',
                                        label: '海珠区'
                                    }
                                ]
                            },
                            {
                                value: 'dongguan',
                                label: '东莞市',
                                children: [
                                    {
                                        value: 'changan',
                                        label: '长安镇'
                                    },
                                    {
                                        value: 'humen',
                                        label: '虎门镇'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        value: 'hunan',
                        label: '湖南省',
                        children: [
                            {
                                value: 'changsha',
                                label: '长沙市',
                                children: [
                                    {
                                        value: 'yuelu',
                                        label: '岳麓区'
                                    }
                                ]
                            }
                        ]
                    }
                ],
                form: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: true,
                    type: ['步步高'],
                    resource: '小天才',
                    desc: '',
                    options: []
                },
                userResume: {
                    name: '',
                    language: '',
                    username: '',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                },
                userResumeRules: {
                    username: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                        {min: 2, max: 8, message: '长度在 2 到 8 个字符'}
                    ],
                    mobile: [
                        {required: true, message: '请输入手机号码', trigger: 'blur'},
                        {validator: customValidate.isMobile, trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: '请输入邮箱地址', trigger: 'blur'},
                        {validator: customValidate.isEmail, trigger: 'blur'}
                    ],
                    gender: [
                        {required: true, message: '请输入验证码', trigger: 'blur'},
                    ],
                    birthday: [
                        {required: true, message: '请输入出生年月', trigger: 'blur'},
                    ],
                },
                activeNames: ['1'],
                // userResume:{
                //
                //
                // }
            }
        },
        methods: {
            onSubmit() {
                this.$message.success('提交成功！');
            },
            // 保存编辑
            saveEdit() {
                this.editVisible = false;
                this.$message.success(`修改第 ${this.idx + 1} 行成功`);
                if (this.tableData[this.idx].id === this.id) {
                    this.$set(this.tableData, this.idx, this.form);
                } else {
                    for (let i = 0; i < this.tableData.length; i++) {
                        if (this.tableData[i].id === this.id) {
                            this.$set(this.tableData, i, this.form);
                            return;
                        }
                    }
                }
            },
            // handleNodeClick(data,node) {
            //     console.log('data',data);
            //     console.log('node',node)
            // },
            handleChange(val) {
                console.log(this.activeNames)
                console.log(val);
            },
            getResumeInfo() {
                // this.resumeId = this.$store.state.a.resumeId;
                this.resumeId = cookie.getCookie('resumeId');
                console.log('-------getResumeId', this.resumeId)
            }
        },
        components: {
            'Education': Education,
            'WorkExperience': WorkExperience,
            'ProjectExperience': ProjectExperience,
            'Skills': Skills,
            'SelfAppraise': SelfAppraise,
        },
        created() {
            this.getResumeInfo()
        },
        activated() {
            this.getResumeInfo()
        }
    }
</script>
<style scoped>
    .tform {
        font-family: "16px Medium", "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        font-size: 16px;
    }

    /*.align-center{*/
    /*    margin:0 auto;		!* 居中 这个是必须的，，其它的属性非必须 *!*/
    /*}*/

    .box-card-left {
        border: none;
        display: block;
    }

    .text {
        font-size: 20px;
    }

</style>
