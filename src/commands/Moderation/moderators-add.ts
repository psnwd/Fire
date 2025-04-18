import { ApplicationCommandMessage } from "@fire/lib/extensions/appcommandmessage";
import { FireMember } from "@fire/lib/extensions/guildmember";
import { Command } from "@fire/lib/util/command";
import { Language } from "@fire/lib/util/language";
import { PermissionFlagsBits } from "discord-api-types/v9";
import { Role } from "discord.js";
import Moderators from "./moderators";

export default class AddModerator extends Command {
  constructor() {
    super("moderators-add", {
      description: (language: Language) =>
        language.get("MODERATORS_ADD_COMMAND_DESCRIPTION"),
      userPermissions: [PermissionFlagsBits.ManageGuild],
      args: [
        {
          id: "moderator",
          type: "member|role",
          readableType: "member/role",
          slashCommandType: "member-or-role",
          default: null,
          required: true,
        },
      ],
      parent: "moderators",
      slashOnly: true,
    });
  }

  async run(
    command: ApplicationCommandMessage,
    args: { moderator: FireMember | Role }
  ) {
    let current = command.guild.settings.get<string[]>("utils.moderators", []);
    if (!current.includes(args.moderator.id)) current.push(args.moderator.id);
    else
      return await command.error("MODERATORS_ADD_ALREADY_ADDED", {
        type:
          args.moderator instanceof FireMember
            ? command.language.get("MEMBER")
            : command.language.get("ROLE"),
      });
    if (current.length)
      await command.guild.settings.set<string[]>(
        "utils.moderators",
        current,
        command.author
      );
    else
      await command.guild.settings.delete("utils.moderators", command.author);
    return await (this.parentCommand as Moderators).getModeratorEmbed(command);
  }
}
