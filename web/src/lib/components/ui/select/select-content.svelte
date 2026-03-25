<script lang="ts">
	import { Select as SelectPrimitive } from "bits-ui";
	import SelectScrollUpButton from "./select-scroll-up-button.svelte";
	import SelectScrollDownButton from "./select-scroll-down-button.svelte";
	import { cn, type WithoutChild } from "$lib/utils.js";

	let {
		ref = $bindable(null),
		class: className,
		sideOffset = 6,
		children,
		...restProps
	}: WithoutChild<SelectPrimitive.ContentProps> = $props();
</script>

<SelectPrimitive.Content
	bind:ref
	{sideOffset}
	data-slot="select-content"
	class={cn(
		"bg-popover text-popover-foreground border-border relative z-50 max-h-[min(var(--bits-select-content-available-height,24rem),24rem)] min-w-[var(--bits-select-anchor-width)] overflow-hidden rounded-md border shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
		className
	)}
	{...restProps}
>
	<SelectScrollUpButton />
	<SelectPrimitive.Viewport class="w-full p-1">
		{@render children?.()}
	</SelectPrimitive.Viewport>
	<SelectScrollDownButton />
</SelectPrimitive.Content>
