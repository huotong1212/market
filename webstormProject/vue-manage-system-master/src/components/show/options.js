import yaml from 'js-yaml';
import {
    PERSON
} from '../../resume/data.yml';
import {
    terms
} from '../../terms';
import {getAnother, getShowResume} from "../api/api";
import {provinceAndCityData, REGION_DATA, CodeToText} from 'element-china-area-data'

// Called by templates to decrease redundancy
function getVueOptions(name) {
    const opt = {
        name: name,
        data() {
            return {
                person: yaml.load(PERSON),
                terms: terms,
                code: '',
                userResume: {
                    username: '',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                    portrait: '',
                },
                expectation: {
                    job: '',
                    province: '',
                    city: '',
                    salary_min: '',
                    salary_max: '',
                    duty_time: '',
                },
                options: provinceAndCityData,
                selectedOptions: [],
                dutyTimeChoice: {
                    1: '一个月内到岗',
                    2: '两个月内到岗',
                    3: '一周内到岗',
                },
                education: [],
                activeNames: ['1'],
                workExperience: [],
                projectExperience: [],
                tecnology: {
                    1: '前端',
                    3: '后端',
                    4: '数据库',
                },
                texts: ['了解', '熟练', '精通', '大牛',],
                skills: [],
                textarea: '',
                appraise: {},
                language: 0,
            };
        },
        computed: {
            lang() {
                const defaultLang = this.terms.en;
                const useLang = this.terms[this.$store.state.a.lang];

                // overwrite non-set fields with default lang
                Object.keys(defaultLang)
                    .filter(k => !useLang[k])
                    .forEach(k => {
                        console.log(k);
                        useLang[k] = defaultLang[k];
                    });
                this.language = this.$store.state.a.lang
                return useLang;
            },

            contactLinks() {
                const links = {};

                if (this.person.contact.github) {
                    links.github = `https://github.com/${this.person.contact.github}`;
                }

                if (this.person.contact.codefights) {
                    links.codefights = `https://codefights.com/profile/${this.person.contact.codefights}`;
                }

                if (this.person.contact.medium) {
                    links.medium = `https://medium.com/@${this.person.contact.medium}`;
                }

                if (this.person.contact.email) {
                    links.email = `mailto:${this.person.contact.email}`;
                }

                if (this.person.contact.linkedin) {
                    links.linkedin = `https://linkedin.com/in/${this.person.contact.linkedin}`;
                }

                if (this.person.contact.phone) {
                    links.phone = `tel:${this.person.contact.phone}`;
                }

                return links;
            },

            classification() {
                return Object.keys(this.dutyTimeChoice)
            },
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
            city() {
                let province = CodeToText[this.expectation.province]
                let city = CodeToText[this.expectation.city]
                return province+'/'+city
            }
        },
        components:{

        },
        watch:{
          //   language(val){
          //     switch (val) {
          //         case 'cn':
          //             this.getShowResume()
          //             break;
          //         case 'en':
          //             this.getAnother(1)
          //             break;
          //         case 'ja':
          //             this.getAnother(2)
          //             break;
          //     }
          // }
        },
        methods: {
            GetRequest() {
                //let url = window.location.search; //获取url中"?"符后的字串
                let url2 = window.location.href
                let index = url2.indexOf("?")
                if (index != -1) {  //判断是否有参数
                    let str = url2.substr(index + 1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
                    this.code = str.split("=")[1];  //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
                    console.log(this.code);     //直接弹出第一个参数 （如果有多个参数 还要进行循环的）
                }
            },
            getShowResume() {
                getShowResume(
                    {
                        code: this.code
                    }
                ).then((response) => {
                    console.log('getShowResume', response)
                    this.setInfo(response)
                }).catch(function (error) {
                })
            },
            getAnother(language){
                getAnother(
                    {
                        code: this.code,
                        language: language
                    }
                ).then((response) => {
                    console.log('getAnother', response)
                    this.setInfo(response)
                }).catch(function (error) {
                })
            },
            setUserResume(response) {
                this.userResume.username = response.data.username
                this.userResume.mobile = response.data.mobile
                this.userResume.email = response.data.email
                this.userResume.gender = response.data.gender
                this.userResume.birthday = response.data.birthday
                this.userResume.portrait = response.data.portrait

                // 设置简历名称
                this.$store.commit('setResumeName', response.data.name);
            },
            setExpectation(response) {
                this.expectation = response.data.expectation
                this.selectedOptions = [this.expectation.province, this.expectation.city]

            },
            dealChange(value) {
                console.log(value)
                // code转汉字大对象
                this.expectation.province = value[0]
                this.expectation.city = value[1]
                // this.expectation.city = CodeToText[value[1]]
            },
            setInfo(response){
                this.setUserResume(response)
                this.setExpectation(response)
                this.education = response.data.education
                this.workExperience = response.data.work
                this.projectExperience = response.data.project
                this.skills = response.data.skills
                this.appraise = response.data.appraise
                this.$refs.portrait.style['background-image'] = 'url(' + this.userResume.portrait + ')'
            }
        },
        mounted() {
            this.GetRequest()
            this.getShowResume()

        }
    };
    return opt;
}

export {
    getVueOptions
};
