<script lang="ts">
	import { Dialog as DialogPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	let {
		class: className,
		children,
		...restProps
	}: DialogPrimitive.ContentProps = $props();
</script>

<DialogPrimitive.Portal>
	<DialogPrimitive.Overlay
		class="fixed inset-0 z-50 bg-black/80 data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0"
	/>
	<DialogPrimitive.Content
		class={cn(
			"bg-background fixed inset-x-0 bottom-0 z-50 mt-24 flex h-auto max-h-[80vh] flex-col rounded-t-xl border-t",
			"data-open:animate-in data-open:slide-in-from-bottom data-closed:animate-out data-closed:slide-out-to-bottom",
			"duration-300",
			className
		)}
		{...restProps}
	>
		<div class="bg-muted mx-auto mt-4 h-1.5 w-[100px] shrink-0 rounded-full"></div>
		{@render children?.()}
	</DialogPrimitive.Content>
</DialogPrimitive.Portal>
