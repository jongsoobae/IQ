<template>
  <div>
    <v-card flat>
      <v-text-field
        v-model="inputName"
        append-outer-icon="mdi-send"
        :prepend-icon="icon"
        filled
        autofocus
        clear-icon="mdi-close-circle"
        clearable
        label="면접자 추가"
        type="text"
        v-on:keyup.enter="onAddNew"
        @click:append-outer="onAddNew"
      ></v-text-field>
    </v-card>
    <v-card>
      <v-list two-line subheader>
        <v-subheader>
          Today
        </v-subheader>
        <v-divider></v-divider>
        <PersonItem
          v-for="(item, name) in todayItems"
          :key="name"
          :person-info="item"
          @delete-person="deletePerson"
        ></PersonItem>

        <v-subheader>
          Previous
        </v-subheader>
        <v-divider></v-divider>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'
import PersonItem from '@/components/PersonItem'
const contents = [
  `
python dict 의 time complexity 는?
- O(1)
  `,
  `
세션과 쿠키의 차이가 무엇인지 설명하시오.
- 세션은 서버에 저장되는 정보.
- 쿠키는 클라이언트에 저장되는 정보.
  `,
  `
세션방식의 인증과 토큰 방식의 인증 의 차이를 설명하시오.
- 세션방식은 서버에 세션정보를 저장해놓고 매 request 마다 sessionid 가 존재하는지 체크함.
  - revoke 가능, stateless 하지 않음.
  - stateless (서버 scaleout 용이), revoke 불가.
  `,
  `
python GIL 에 대해서 설명하시오. (cpython 한정)
- 여러 쓰레드가 하나의 python object 에 동시에 접근하지 못하게 하는것.
GIL 의 장단점은?
- 장점: cpython 구현이 용이.
- 단점: 쓰레드 대신 프로세스 를 쓰는것에 대한 이야기.
  `
]

const questions = contents.map((c) => ({ content: c, asked: false }))

export default {
  components: {
    PersonItem
  },
  data: () => ({
    inputName: '',
    todayItems: {
      김춘구: {
        name: '김춘구',
        questions
      },
      최다운: {
        name: '최다운',
        questions
      },
      강호동: {
        name: '강호동',
        questions
      },
      유재석: {
        name: '유재석',
        questions
      }
    }
  }),
  methods: {
    onAddNew(ev) {
      if (!this.inputName) {
        ev.target.focus()
        return
      }

      const name = this.inputName
      Vue.set(this.todayItems, name, {
        name,
        questions
      })
      this.initialize()
    },
    deletePerson(name) {
      Vue.delete(this.todayItems, name)
    },
    initialize() {
      this.inputName = ''
    }
  }
}
</script>
