"""Houses the InviteUseTracker helper class"""

class InviteUseTracker:
    """Tracks what invite a joining member used
    Attributes:
        original_invites: The list of invites before the new member joined
        new_invites: The list of invites after the new member joined"""

    def __init__(self, original_invites, new_invites):
        """Create a new InviteUseTracker
        Args:
            original_invites: The list of invites before the new member joined
            new_invites: The list of invites after the new member joined"""

        self.original_invites = original_invites
        self.new_invites = new_invites

    def _get_invite_by_code(self, invite_list, code: str):
        """Return an invite with a specific code from a list
        Args:
            invite_list: The list where to find the invite from
            code: The code to find the invite with
        Returns: The invite, if found. None if not found."""

        for invite in invite_list:
            if invite.code == code:
                return invite
        return None

    def check_difference(self):
        """Check the difference between the two provided invite lists
        Returns: The invite that has new uses. None if no changes were detected."""

        for invite in self.original_invites:
            new_invite = self._get_invite_by_code(self.new_invites, invite.code)
            try:
                if invite.uses != new_invite.uses:
                    return new_invite
            except:
                return None
        return None
