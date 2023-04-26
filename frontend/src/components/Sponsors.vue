<template>
    <section id="sponsors">
        <div class="mt-20 text-center">
            <p class="max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-2xl md:max-w-3xl">
                Thanks to our awesome sponsors
            </p>
        </div>
        <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 flex items-center">
            <div class="flex-auto grid grid-cols-2 gap-8 md:grid-cols-6 lg:grid-cols-6">

                <Sponsor sponsor-name="Horizon Digital" sponsor-type="Major Sponsor" sponsor-url="https://horizondigital.au/" :sponsorImageUrl="horizonLogo" />

                <Sponsor sponsor-name="Ben Fitzhardinge" sponsor-type="Hosting Sponsor" sponsor-url="https://benjamin.dog/" :sponsorImageUrl="BenLogo" />

                <Sponsor sponsor-name="Spacecubed" sponsor-type="Venue Sponsor" sponsor-url="https://spacecubed.com/" :sponsorImageUrl="SpacecubedLogo" />

            </div>
        </div>
    </section>
</template>

<script>
import { ChatIcon } from "@heroicons/vue/outline";
import Sponsor from "./Sponsor.vue";
import HorizonLogo from "../assets/horizon_logo_sig.png";
import SpacecubedLogo from "../assets/spacecubed.png";
import BenLogo from "../assets/benjamin_dog.png";
export default {
    components: {
      Sponsor,
      ChatIcon,
      HorizonLogo,
    },
  data() {
    return {
      horizonLogo: HorizonLogo,
      SpacecubedLogo,
      BenLogo,
    }
  }
};
</script>    
