def suggestCompatibleCPUs(userBuild, cpuComp):
    from pc_builder.components.cpu import loadCPUsfromJSON

    suggestedCPUs = []
    allCPUs = loadCPUsfromJSON()

    for cpu in allCPUs:
        isCompatible, compatibility = cpu.checkCompatibility(userBuild)

        if len(suggestedCPUs) == 6:
            break
        if isCompatible:
            suggestedCPUs.append(cpu)

    return suggestedCPUs[:5]
