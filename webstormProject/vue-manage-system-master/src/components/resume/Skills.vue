<template>
    <div>
        <!--允许多个技能-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item v-for="[key,item] in data" :key="key" name="key">
                <template slot="title">
                    <span style="width: 95%">
                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{tecnology[key]}}</span>
                    </span>
                    <el-button type="text" @click="showForm(key)" icon="el-icon-plus">添加</el-button>
                    <el-button @click="deleteThisCategory(key)" type="text" icon="el-icon-delete">删除</el-button>

                </template>

                <!--Skills-->
                <div class="e-rate" v-for="skill of item">
                    <el-input :disabled="true" placeholder="请输入内容" v-model="skill.skill_desc" style="width: 70%">
                        <template slot="prepend">{{skill.skill_tag}}</template>
                    </el-input>
                    &emsp;&emsp;&emsp;
                    <el-rate :disabled="true" class="e-rate" v-model="skill.skill_level" show-text :max=4
                             :texts="texts">
                    </el-rate>
                    &ensp;&ensp;&ensp;&ensp;
                    <el-button type="text" @click="showUpdateSkills(skill.id)" icon="el-icon-edit">编辑</el-button>
                    <el-button type="text" @click="deleteThisSkill(skill.id)" icon="el-icon-delete" class="red">删除
                    </el-button>
                </div>
            </el-collapse-item>
        </el-collapse>

        <!-- 创建技能弹出框 -->
        <el-dialog :title="createOrUpdate === 'update'?'更新技能特长':'创建技能特长'" :visible.sync="createVisible" width="30%">
            <el-form ref="form" :rules="rules" :model="form" status-icon label-width="80px">
                <el-form-item label="技能分类" prop="category">
                    <el-select v-model="form.category" placeholder="请选择技能类别">
                        <el-option v-for="index in classification" :key="Number(index)" :label="tecnology[index]" :value="Number(index)"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="标签" prop="skill_tag">
                    <el-input v-model="form.skill_tag" maxlength="20" placeholder="请输入标签"></el-input>
                </el-form-item>
                <el-form-item label="技能描述" prop="skill_desc">
                    <el-input v-model="form.skill_desc" maxlength="50" placeholder="请输入技能描述"></el-input>
                </el-form-item>
                <el-form-item label="熟悉程度" prop="skill_level">
                    <el-rate class="e-rate" v-model="form.skill_level" show-text :max=4
                             :texts="texts">
                    </el-rate>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="createVisible = false">取 消</el-button>
                <el-button type="primary" @click="createOrUpdateSkills('form')">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {createSkills, deleteSkills, getAllSkills, updateSkills} from "../api/api";
    import cookie from "../static/cookie";

    export default {
        name: "Skills",
        data: function () {
            return {
                resumeId: '',
                activeNames: ['1'],
                skills: [
                    {
                        "id": 1,
                        "skill_tag": "Vue",
                        "skill_desc": "熟悉Vue",
                        "skill_level": 2,
                        "category": 1,
                        "resume_id": 1
                    },
                    {
                        "id": 2,
                        "skill_tag": "Angular",
                        "skill_desc": "了解Angular",
                        "skill_level": 1,
                        "category": 1,
                        "resume_id": 1
                    },
                    {
                        "id": 3,
                        "skill_tag": "Django",
                        "skill_desc": "熟悉Django",
                        "skill_level": 2,
                        "category": 3,
                        "resume_id": 1
                    }
                ],
                form: {
                    id:'',
                    skill_tag: "Django",
                    skill_desc: "熟悉Django",
                    skill_level: 2,
                    category: '',
                    resume_id: '',
                },
                rules: {
                    skill_tag: [
                        {max: 20, message: '长度在 20 个字符之内'}
                    ],
                    skill_desc: [
                        {max: 50, message: '长度在 50 个字符之内'}
                    ],
                },
                tecnology: {
                    1: '前端',
                    3: '后端',
                    4: '数据库',
                },
                level: {
                    '1': '了解',
                    '2': '熟练',
                    '3': '精通',
                    '4': '大牛',
                },
                texts: ['了解', '熟练', '精通', '大牛',],
                createVisible: false,
                createOrUpdate:'',
            }
        },

        methods: {
            handleChange(val) {
                //console.log('this.data', this.data)
                // console.log(this.activeNames)
                // console.log(val);
            },
            getAllSkills() {
                getAllSkills(
                    this.resumeId
                ).then((response) => {
                    //箭头函数中的this是这个vue对象
                    this.skills = response.data
                }).catch(function (error) {

                });
            },
            deleteThisSkill(skillId) {
                const index = this.skills.findIndex(item => item.id === skillId);
                deleteSkills(
                    skillId,
                    {}
                ).then((response) => {
                    this.skills.splice(index, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                }).catch(function (error) {

                })
            },
            deleteThisCategory(categoryId) {
                let item = this.skills.find(item => item.category === categoryId);
                // 传一个存在的skill的id，不然会抛出404错误
                deleteSkills(item.id,
                    {
                        category: categoryId,
                        resumeId: this.resumeId
                    }
                ).then((response) => {
                    console.log('deleteSkills', response)
                    this.clearSkills(categoryId)
                }).catch(function (error) {

                })
            },
            // 点击添加
            showForm(category){
                this.form.category = category
                this.createVisible = true
                this.createOrUpdate = 'create'
            },
            // 点击编辑
            showUpdateSkills(id) {
                let skill = this.skills.find(item => item.id === id);
                this.form = skill
                this.createVisible = true
                this.createOrUpdate = 'update'
            },

            createOrUpdateSkills(formName){
                if(this.createOrUpdate === 'update'){
                    this.updateSkills()
                } else if (this.createOrUpdate === 'create'){
                    this.createSkills(formName)
                }
            },

            createSkills(formName) {
                this.form.resume_id = this.resumeId
                // if(this.form.hasOwnProperty('id')){
                //     delete this.form.id
                // }
                // console.log('form',this.form)

                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        createSkills(
                            this.form
                        ).then((response) => {
                            console.log('createSkills', response)
                            this.skills.push(response.data)
                            this.createVisible = false
                        }).catch(function (error) {
                            // console.log(error)
                        })
                    }
                })
            },

            updateSkills(){
                //this.$refs.form.validate((valid) => {
                //if (valid) {
                let skill = this.skills.find(item => item.id === this.form.id)

                updateSkills(this.form.id,
                    this.form
                ).then((response) => {
                    console.log('updateSkills', response)
                    skill = response.data
                    this.createVisible = false
                }).catch(function (error) {
                    // console.log(error)
                })

                //}
                //})
            },

            clearSkills(categoryId) {
                while (true) {
                    let index = this.skills.findIndex(item => item.category === categoryId);
                    if (index === -1) {
                        break;
                    } else {
                        this.skills.splice(index, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                    }
                }
            }
        },
        computed: {
            data() {
                let data = new Map();
                this.skills.forEach(function (element, index) {
                    // console.log(element); // red green blue
                    // console.log(index);   // 0 1 2

                    // 转为int,因为在Set中的key最好为基础类型，2个不同的对象被认为是2个key
                    let category = Number.parseInt(element.category)

                    // 判断是否被添加过
                    if (!data.has(category)) {
                        data.set(category, [])
                    }

                    data.get(category).push(element)
                });
                return data
            },
            rate: {
                get: function () {
                    return function (key) {
                        const levels = new Map([
                            ['1', '了解'],
                            ['2', '熟练'],
                            ['3', '精通'],
                            ['4', '大牛'],
                        ])
                        return levels.get(key)
                    }
                },
                set: function (newValue) {

                }

            },
            classification() {
                return Object.keys(this.tecnology)
            }
        },
        mounted() {
            this.resumeId = cookie.getCookie('resumeId')
            this.getAllSkills()
        }

    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium", "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        font-size: 16px;
    }

    .e-rate {
        /*float: left;*/
        display: inline;
    }
</style>
