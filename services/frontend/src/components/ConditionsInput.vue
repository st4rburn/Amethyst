<script setup lang="ts">
defineProps(['name', 'type', 'label', 'conditions', 'desc'])
</script>

<template>
    <div :id="name + '-conditions'" :class="{fulfilled: complete, hidden: hidden, 'conditions-box': true}">
        <p>Requirements:</p>
        <ul>
            <li v-for="item of items" :class="{fulfilled: item.fulfilled}">
                <span class="cross-bullet" :style="(!item.fulfilled ? 'display: inline;' : 'display: none;')" v-html="cross_svg"></span>
                <span class="tick-bullet" :style="(item.fulfilled ? 'display: inline;' : 'display: none;')" v-html="tick_svg"></span>
                {{ item.text }}
            </li>
        </ul>
    </div>
    <label :for="name">{{ label }} <i v-if="desc">{{ desc }}</i></label><input :id="name + '-field'" :name="name" required :type="type" @input="check" @focus="validation_info" @blur="validation_info">
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import cross_svg from '@/assets/cross.svg?raw';
import tick_svg from '@/assets/tick.svg?raw';

export default defineComponent({
    name: "ConditionsInput",
    methods: {
        // As soon as one condition is unfulfilled, the rest are no longer updated
        //   (usually the first to be broken shows it, but if two are broken at the same time it is reflected)
        // Only updated initially when all fields are fulfilled
        
        // internal elements only update when external is updated

        // Check all conditions are met
        check(e: Event): boolean {
            let result = true;
            for (let condition of this.items) {
                condition.fulfilled = condition.condition((e.target as HTMLFormElement).value);
                if (!condition.fulfilled) {
                    result = false;
                }
            }

            this.complete = result;
            return result;
        },

        validation_info(e: FocusEvent) {
            if (e.type === "focus") {
                this.hidden = false;
            } else {
                this.hidden = this.complete;
            }
        }
    },

    data() {
        let items = [];
        for (let item of this.conditions) {
            items.push({
                text: item.text,
                condition: item.condition,
                fulfilled: false
            });
        }
        return {
            items,
            hidden: true,
            complete: false,
            cross_svg,
            tick_svg,
        };
    },
});
</script>

<style scoped>
div.conditions-box {
    border-left: var(--red) 3px solid;
    padding-left: 16px;
    margin-bottom: 12px;
}
div.conditions-box.hidden {
    display: none;
}
div.conditions-box.fulfilled {
    border-left: var(--green) 3px solid;
    padding-left: 16px;
    margin-bottom: 12px;
}

div.conditions-box ul {
    margin-left: 0px;
    padding: 0px;
    list-style-type: none;
}
div.conditions-box >>> svg {
    position: relative;
    vertical-align: top;
    top: 0.3em;
    height: 1.2em;
    fill: red;
}
div.conditions-box li >>> svg {
    fill: var(--red);
    /*&.cross-bullet {
        display: inline;
    }
    &.tick-bullet {
        display: none;
    }*/
}
div.conditions-box li.fulfilled >>> svg {
    fill: var(--green);
    /*&.cross-bullet {
        display: none;
    }
    &.tick-bullet {
        display: inline;
    }*/
}
</style>