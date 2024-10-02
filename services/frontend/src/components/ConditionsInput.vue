<script setup lang="ts">
defineProps(['name', 'type', 'label', 'conditions', 'desc'])
</script>

<template>
    <div :id="name + '-conditions'" :class="{fulfilled: complete, pending: pending, hidden: hidden, 'conditions-box': true}">
        <p>Requirements:</p>
        <ul>
            <li v-for="item of items" :class="{fulfilled: item.state == ConditionState.Fulfilled, pending: item.state == ConditionState.Pending}">
                <span class="clock-bullet" :style="(item.state == ConditionState.Pending ? 'display: inline;' : 'display: none;')" v-html="clock_svg"></span>
                <span class="cross-bullet" :style="(item.state == ConditionState.Unfulfilled ? 'display: inline;' : 'display: none;')" v-html="cross_svg"></span>
                <span class="error-bullet" :style="(item.state == ConditionState.Error ? 'display: inline;' : 'display: none;')" v-html="error_svg"></span>
                <span class="tick-bullet" :style="(item.state == ConditionState.Fulfilled ? 'display: inline;' : 'display: none;')" v-html="tick_svg"></span>
                {{ item.text }}
            </li>
        </ul>
    </div>
    <label :for="name">{{ label }} <i v-if="desc">{{ desc }}</i></label><input :id="name + '-field'" :name="name" required :type="type" @input="check" @focus="validation_info" @blur="validation_info">
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import clock_svg from '@/assets/clock.svg?raw';
import cross_svg from '@/assets/cross.svg?raw';
import error_svg from '@/assets/error.svg?raw';
import tick_svg from '@/assets/tick.svg?raw';

export enum ConditionState {
    Unfulfilled,
    Fulfilled,
    Pending,
    Error
}

export default defineComponent({
    name: "ConditionsInput",
    methods: {
        // As soon as one condition is unfulfilled, the rest are no longer updated
        //   (usually the first to be broken shows it, but if two are broken at the same time it is reflected)
        // Only updated initially when all fields are fulfilled
        
        // internal elements only update when external is updated

        // Check all conditions are met
        check(e: Event) {
            for (let condition of this.items) {
                // Check dependencies first (all dependencies should be above this condition)
                // This will get janky with async dependencies, we don't worry about that for now
                // One solution could be to give every condition a promise that fulfils when it completes? And then resolve all conditions
                // asynchronously after their dependencies finish
                let run_check = true;
                for (let index of condition.deps) {
                    if (this.items[index].state != ConditionState.Fulfilled) {
                        condition.state = ConditionState.Pending;
                        run_check = false;
                        break;
                    }
                }
                if (run_check) {
                    // Do we need to provide callback options?
                    if (condition.callback) {
                        // Provide a callback function to apply the result
                        condition.state = ConditionState.Pending;
                        condition.condition((e.target as HTMLFormElement).value, (answer: ConditionState) => {
                            condition.state = answer;
                            // Remember to update the state of the whole box after changing state
                            this.update_whole();
                        });
                    } else {
                        condition.state = condition.condition((e.target as HTMLFormElement).value) ? ConditionState.Fulfilled : ConditionState.Unfulfilled;
                    }
                }
            }

            this.update_whole();
        },

        update_whole() {
            let result = true;
            let pending = true;
            for (let condition of this.items) {
                if (condition.state != ConditionState.Fulfilled) {
                    result = false;
                    if (condition.state != ConditionState.Pending) {
                        pending = false;
                    }
                }
            }
            this.complete = result;
            this.pending = this.complete ? false : pending;
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
                state: ConditionState.Pending,
                callback: "callback" in item ? item.callback : false,
                deps: "deps" in item ? item.deps : [],
            });
        }
        return {
            items,
            hidden: true,
            complete: false,
            pending: true,
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
}
div.conditions-box.pending {
    border-left: var(--amber) 3px solid;
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
div.conditions-box li.pending >>> svg {
    fill: var(--amber);
    /*&.cross-bullet {
        display: none;
    }
    &.tick-bullet {
        display: inline;
    }*/
}
</style>