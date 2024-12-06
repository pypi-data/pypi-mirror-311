import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_constituencies_display_order import ConstituentConstituenciesDisplayOrder
    from ..models.constituent_social_media_accounts import ConstituentSocialMediaAccounts
    from ..models.constituent_student_relation_constituencies import ConstituentStudentRelationConstituencies
    from ..models.constituent_user_defined_constituencies import ConstituentUserDefinedConstituencies
    from ..models.fuzzy_date import FuzzyDate


T = TypeVar("T", bound="ConstituentSummaryProfileView")


@_attrs_define
class ConstituentSummaryProfileView:
    """ViewConstituentSummaryProfile.

    Attributes:
        constituent_profile (Union[Unset, bool]): Indicates whether isconstituentprofile.
        organization (Union[Unset, bool]): Indicates whether isorganization.
        address (Union[Unset, str]): The address.
        phone_number (Union[Unset, str]): The phonenumber.
        phone_type (Union[Unset, str]): The phonetype.
        email_address (Union[Unset, str]): The emailaddress.
        do_not_mail (Union[Unset, bool]): Indicates whether donotmail.
        do_not_email (Union[Unset, bool]): Indicates whether donotemail.
        do_not_phone (Union[Unset, bool]): Indicates whether donotphone.
        web_address (Union[Unset, str]): The webaddress.
        related_constituent (Union[Unset, str]): The relatedconstituent.
        related_constituent_id (Union[Unset, str]): The relatedconstituentid.
        plannedgiverconstituencytext (Union[Unset, str]): The plannedgiverconstituencytext.
        bank_constituency_text (Union[Unset, str]): The bankconstituencytext.
        recognition_constituency_text (Union[Unset, str]): The recognitionconstituencytext.
        student_enrollment_id (Union[Unset, str]): The studentenrollmentid.
        student_constituency_text (Union[Unset, str]): The studentconstituencytext.
        member_constituency_text (Union[Unset, str]): The memberconstituencytext.
        advocate_constituency_text (Union[Unset, str]): The advocateconstituencytext.
        board_member_constituency_text (Union[Unset, str]): The boardmemberconstituencytext.
        relation_constituency_text (Union[Unset, str]): The relationconstituencytext.
        staff_constituency_text (Union[Unset, str]): The staffconstituencytext.
        donor_constituency_text (Union[Unset, str]): The donorconstituencytext.
        fundraiser_constituency_text (Union[Unset, str]): The fundraiserconstituencytext.
        prospect_constituency_text (Union[Unset, str]): The prospectconstituencytext.
        volunteer_constituency_text (Union[Unset, str]): The volunteerconstituencytext.
        patron_constituency_text (Union[Unset, str]): The patronconstituencytext.
        community_member_constituency_text (Union[Unset, str]): The communitymemberconstituencytext.
        user_defined_constituency_text (Union[Unset, str]): The userdefinedconstituencytext.
        alumnus_status_text (Union[Unset, str]): The alumnusstatustext.
        alumnus_enrollment_id (Union[Unset, str]): The alumnusenrollmentid.
        alumnus_constituency_text (Union[Unset, str]): The alumnusconstituencytext.
        registrant_status_text (Union[Unset, str]): The registrantstatustext.
        vendor_status_text (Union[Unset, str]): The vendorstatustext.
        inactive (Union[Unset, bool]): Indicates whether isinactive.
        deceaseddate (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        picture (Union[Unset, str]): The picture.
        primary_education_id (Union[Unset, str]): The primaryeducationid.
        primary_education (Union[Unset, str]): The primary education.
        primary_business_id (Union[Unset, str]): The primarybusinessid.
        primary_business (Union[Unset, str]): The primary business.
        lookup_id (Union[Unset, str]): The lookup ID.
        wealthpoint_update_pending (Union[Unset, bool]): Indicates whether wealthpointupdatepending.
        education_attribute_defined (Union[Unset, bool]): Indicates whether educationattributedefined.
        matchfinder_constituency_text (Union[Unset, str]): The matchfinderconstituencytext.
        matchfinder_online_record_id (Union[Unset, int]): The matchfinderonlinerecordid.
        solicit_code_count (Union[Unset, int]): The solicitcodecount.
        household_id (Union[Unset, str]): The householdid.
        household_text (Union[Unset, str]): The household.
        group (Union[Unset, bool]): Indicates whether isgroup.
        group_type (Union[Unset, str]): The group type.
        group_member_count (Union[Unset, int]): The no. of members.
        household (Union[Unset, bool]): Indicates whether is household.
        gives_anonymously (Union[Unset, bool]): Indicates whether gives anonymously.
        spouse_deceased (Union[Unset, bool]): Indicates whether is spouse deceased.
        dissolved (Union[Unset, bool]): Indicates whether is group dissolved.
        declarations_on_file (Union[Unset, bool]): Indicates whether declarationsonfile.
        committee_constituency_text (Union[Unset, str]): The committeeconstituencytext.
        committee_member (Union[Unset, bool]): Indicates whether iscommitteemember.
        grantor_constituency_text (Union[Unset, str]): The grantorconstituencytext.
        sponsor_constituency_text (Union[Unset, str]): The sponsorconstituencytext.
        nfg_constituency_text (Union[Unset, str]): The nfgconstituencytext.
        constituent_inactivity_reason (Union[Unset, str]): The inactive reason.
        committee_member_constituency_text (Union[Unset, str]): The committeememberconstituencytext.
        faculty_constituency_text (Union[Unset, str]): The facultyconstituencytext.
        deceased (Union[Unset, bool]): Indicates whether isdeceased.
        current_enrollment_id (Union[Unset, str]): The currentenrollmentid.
        current_school (Union[Unset, str]): The school.
        current_enrollment_id_2 (Union[Unset, str]): The currentenrollmentid2.
        current_school_2 (Union[Unset, str]): The currentschool2.
        current_enrollment_id_3 (Union[Unset, str]): The currentenrollmentid3.
        current_school_3 (Union[Unset, str]): The currentschool3.
        loyal_donor_constituency_text (Union[Unset, str]): The loyaldonorconstituencytext.
        major_donor_constituency_text (Union[Unset, str]): The majordonorconstituencytext.
        student_relation_constituency_text (Union[Unset, str]): The studentrelationconstituencytext.
        phone_is_confidential (Union[Unset, bool]): Indicates whether phoneisconfidential.
        address_is_confidential (Union[Unset, bool]): Indicates whether addressisconfidential.
        constituencies_display_order (Union[Unset, List['ConstituentConstituenciesDisplayOrder']]): Constituencies
            display order.
        sponsor_type_code (Union[Unset, int]): The sponsortypecode.
        lifecycle_stage (Union[Unset, str]): The donor lifecycle.
        lifecycle_stage_as_of (Union[Unset, datetime.datetime]): The as of. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        planned_giver_stage (Union[Unset, str]): The plannedgiverstage.
        planned_giver_stage_as_of (Union[Unset, datetime.datetime]): The as of. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        donor_state_code (Union[Unset, int]): The donorstatecode.
        donor_state (Union[Unset, str]): The donor state.
        last_revenue_date (Union[Unset, datetime.datetime]): The lastrevenuedate. Uses the format YYYY-MM-DDThh:mm:ss.
            An example date: <i>1955-11-05T22:04:00</i>.
        address_id (Union[Unset, str]): The addressid.
        phone_number_id (Union[Unset, str]): The phonenumberid.
        email_address_id (Union[Unset, str]): The emailaddressid.
        top_parent_id (Union[Unset, str]): The topparentid.
        top_parent (Union[Unset, str]): The top parent organization.
        user_defined_constituencies (Union[Unset, List['ConstituentUserDefinedConstituencies']]): User defined
            constituencies.
        student_relation_constituencies (Union[Unset, List['ConstituentStudentRelationConstituencies']]): Student
            relation constituencies.
        user_granted_constitpersonalinfo_edit (Union[Unset, bool]): Indicates whether
            user_granted_constitpersonalinfo_edit.
        name (Union[Unset, str]): The name.
        fundraising_group_constituency_text (Union[Unset, str]): The fundraisinggroupconstituencytext.
        social_media_accounts (Union[Unset, List['ConstituentSocialMediaAccounts']]): Social media accounts.
    """

    constituent_profile: Union[Unset, bool] = UNSET
    organization: Union[Unset, bool] = UNSET
    address: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    phone_type: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    do_not_mail: Union[Unset, bool] = UNSET
    do_not_email: Union[Unset, bool] = UNSET
    do_not_phone: Union[Unset, bool] = UNSET
    web_address: Union[Unset, str] = UNSET
    related_constituent: Union[Unset, str] = UNSET
    related_constituent_id: Union[Unset, str] = UNSET
    plannedgiverconstituencytext: Union[Unset, str] = UNSET
    bank_constituency_text: Union[Unset, str] = UNSET
    recognition_constituency_text: Union[Unset, str] = UNSET
    student_enrollment_id: Union[Unset, str] = UNSET
    student_constituency_text: Union[Unset, str] = UNSET
    member_constituency_text: Union[Unset, str] = UNSET
    advocate_constituency_text: Union[Unset, str] = UNSET
    board_member_constituency_text: Union[Unset, str] = UNSET
    relation_constituency_text: Union[Unset, str] = UNSET
    staff_constituency_text: Union[Unset, str] = UNSET
    donor_constituency_text: Union[Unset, str] = UNSET
    fundraiser_constituency_text: Union[Unset, str] = UNSET
    prospect_constituency_text: Union[Unset, str] = UNSET
    volunteer_constituency_text: Union[Unset, str] = UNSET
    patron_constituency_text: Union[Unset, str] = UNSET
    community_member_constituency_text: Union[Unset, str] = UNSET
    user_defined_constituency_text: Union[Unset, str] = UNSET
    alumnus_status_text: Union[Unset, str] = UNSET
    alumnus_enrollment_id: Union[Unset, str] = UNSET
    alumnus_constituency_text: Union[Unset, str] = UNSET
    registrant_status_text: Union[Unset, str] = UNSET
    vendor_status_text: Union[Unset, str] = UNSET
    inactive: Union[Unset, bool] = UNSET
    deceaseddate: Union[Unset, "FuzzyDate"] = UNSET
    picture: Union[Unset, str] = UNSET
    primary_education_id: Union[Unset, str] = UNSET
    primary_education: Union[Unset, str] = UNSET
    primary_business_id: Union[Unset, str] = UNSET
    primary_business: Union[Unset, str] = UNSET
    lookup_id: Union[Unset, str] = UNSET
    wealthpoint_update_pending: Union[Unset, bool] = UNSET
    education_attribute_defined: Union[Unset, bool] = UNSET
    matchfinder_constituency_text: Union[Unset, str] = UNSET
    matchfinder_online_record_id: Union[Unset, int] = UNSET
    solicit_code_count: Union[Unset, int] = UNSET
    household_id: Union[Unset, str] = UNSET
    household_text: Union[Unset, str] = UNSET
    group: Union[Unset, bool] = UNSET
    group_type: Union[Unset, str] = UNSET
    group_member_count: Union[Unset, int] = UNSET
    household: Union[Unset, bool] = UNSET
    gives_anonymously: Union[Unset, bool] = UNSET
    spouse_deceased: Union[Unset, bool] = UNSET
    dissolved: Union[Unset, bool] = UNSET
    declarations_on_file: Union[Unset, bool] = UNSET
    committee_constituency_text: Union[Unset, str] = UNSET
    committee_member: Union[Unset, bool] = UNSET
    grantor_constituency_text: Union[Unset, str] = UNSET
    sponsor_constituency_text: Union[Unset, str] = UNSET
    nfg_constituency_text: Union[Unset, str] = UNSET
    constituent_inactivity_reason: Union[Unset, str] = UNSET
    committee_member_constituency_text: Union[Unset, str] = UNSET
    faculty_constituency_text: Union[Unset, str] = UNSET
    deceased: Union[Unset, bool] = UNSET
    current_enrollment_id: Union[Unset, str] = UNSET
    current_school: Union[Unset, str] = UNSET
    current_enrollment_id_2: Union[Unset, str] = UNSET
    current_school_2: Union[Unset, str] = UNSET
    current_enrollment_id_3: Union[Unset, str] = UNSET
    current_school_3: Union[Unset, str] = UNSET
    loyal_donor_constituency_text: Union[Unset, str] = UNSET
    major_donor_constituency_text: Union[Unset, str] = UNSET
    student_relation_constituency_text: Union[Unset, str] = UNSET
    phone_is_confidential: Union[Unset, bool] = UNSET
    address_is_confidential: Union[Unset, bool] = UNSET
    constituencies_display_order: Union[Unset, List["ConstituentConstituenciesDisplayOrder"]] = UNSET
    sponsor_type_code: Union[Unset, int] = UNSET
    lifecycle_stage: Union[Unset, str] = UNSET
    lifecycle_stage_as_of: Union[Unset, datetime.datetime] = UNSET
    planned_giver_stage: Union[Unset, str] = UNSET
    planned_giver_stage_as_of: Union[Unset, datetime.datetime] = UNSET
    donor_state_code: Union[Unset, int] = UNSET
    donor_state: Union[Unset, str] = UNSET
    last_revenue_date: Union[Unset, datetime.datetime] = UNSET
    address_id: Union[Unset, str] = UNSET
    phone_number_id: Union[Unset, str] = UNSET
    email_address_id: Union[Unset, str] = UNSET
    top_parent_id: Union[Unset, str] = UNSET
    top_parent: Union[Unset, str] = UNSET
    user_defined_constituencies: Union[Unset, List["ConstituentUserDefinedConstituencies"]] = UNSET
    student_relation_constituencies: Union[Unset, List["ConstituentStudentRelationConstituencies"]] = UNSET
    user_granted_constitpersonalinfo_edit: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    fundraising_group_constituency_text: Union[Unset, str] = UNSET
    social_media_accounts: Union[Unset, List["ConstituentSocialMediaAccounts"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_profile = self.constituent_profile

        organization = self.organization

        address = self.address

        phone_number = self.phone_number

        phone_type = self.phone_type

        email_address = self.email_address

        do_not_mail = self.do_not_mail

        do_not_email = self.do_not_email

        do_not_phone = self.do_not_phone

        web_address = self.web_address

        related_constituent = self.related_constituent

        related_constituent_id = self.related_constituent_id

        plannedgiverconstituencytext = self.plannedgiverconstituencytext

        bank_constituency_text = self.bank_constituency_text

        recognition_constituency_text = self.recognition_constituency_text

        student_enrollment_id = self.student_enrollment_id

        student_constituency_text = self.student_constituency_text

        member_constituency_text = self.member_constituency_text

        advocate_constituency_text = self.advocate_constituency_text

        board_member_constituency_text = self.board_member_constituency_text

        relation_constituency_text = self.relation_constituency_text

        staff_constituency_text = self.staff_constituency_text

        donor_constituency_text = self.donor_constituency_text

        fundraiser_constituency_text = self.fundraiser_constituency_text

        prospect_constituency_text = self.prospect_constituency_text

        volunteer_constituency_text = self.volunteer_constituency_text

        patron_constituency_text = self.patron_constituency_text

        community_member_constituency_text = self.community_member_constituency_text

        user_defined_constituency_text = self.user_defined_constituency_text

        alumnus_status_text = self.alumnus_status_text

        alumnus_enrollment_id = self.alumnus_enrollment_id

        alumnus_constituency_text = self.alumnus_constituency_text

        registrant_status_text = self.registrant_status_text

        vendor_status_text = self.vendor_status_text

        inactive = self.inactive

        deceaseddate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deceaseddate, Unset):
            deceaseddate = self.deceaseddate.to_dict()

        picture = self.picture

        primary_education_id = self.primary_education_id

        primary_education = self.primary_education

        primary_business_id = self.primary_business_id

        primary_business = self.primary_business

        lookup_id = self.lookup_id

        wealthpoint_update_pending = self.wealthpoint_update_pending

        education_attribute_defined = self.education_attribute_defined

        matchfinder_constituency_text = self.matchfinder_constituency_text

        matchfinder_online_record_id = self.matchfinder_online_record_id

        solicit_code_count = self.solicit_code_count

        household_id = self.household_id

        household_text = self.household_text

        group = self.group

        group_type = self.group_type

        group_member_count = self.group_member_count

        household = self.household

        gives_anonymously = self.gives_anonymously

        spouse_deceased = self.spouse_deceased

        dissolved = self.dissolved

        declarations_on_file = self.declarations_on_file

        committee_constituency_text = self.committee_constituency_text

        committee_member = self.committee_member

        grantor_constituency_text = self.grantor_constituency_text

        sponsor_constituency_text = self.sponsor_constituency_text

        nfg_constituency_text = self.nfg_constituency_text

        constituent_inactivity_reason = self.constituent_inactivity_reason

        committee_member_constituency_text = self.committee_member_constituency_text

        faculty_constituency_text = self.faculty_constituency_text

        deceased = self.deceased

        current_enrollment_id = self.current_enrollment_id

        current_school = self.current_school

        current_enrollment_id_2 = self.current_enrollment_id_2

        current_school_2 = self.current_school_2

        current_enrollment_id_3 = self.current_enrollment_id_3

        current_school_3 = self.current_school_3

        loyal_donor_constituency_text = self.loyal_donor_constituency_text

        major_donor_constituency_text = self.major_donor_constituency_text

        student_relation_constituency_text = self.student_relation_constituency_text

        phone_is_confidential = self.phone_is_confidential

        address_is_confidential = self.address_is_confidential

        constituencies_display_order: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.constituencies_display_order, Unset):
            constituencies_display_order = []
            for constituencies_display_order_item_data in self.constituencies_display_order:
                constituencies_display_order_item = constituencies_display_order_item_data.to_dict()
                constituencies_display_order.append(constituencies_display_order_item)

        sponsor_type_code = self.sponsor_type_code

        lifecycle_stage = self.lifecycle_stage

        lifecycle_stage_as_of: Union[Unset, str] = UNSET
        if not isinstance(self.lifecycle_stage_as_of, Unset):
            lifecycle_stage_as_of = self.lifecycle_stage_as_of.isoformat()

        planned_giver_stage = self.planned_giver_stage

        planned_giver_stage_as_of: Union[Unset, str] = UNSET
        if not isinstance(self.planned_giver_stage_as_of, Unset):
            planned_giver_stage_as_of = self.planned_giver_stage_as_of.isoformat()

        donor_state_code = self.donor_state_code

        donor_state = self.donor_state

        last_revenue_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_revenue_date, Unset):
            last_revenue_date = self.last_revenue_date.isoformat()

        address_id = self.address_id

        phone_number_id = self.phone_number_id

        email_address_id = self.email_address_id

        top_parent_id = self.top_parent_id

        top_parent = self.top_parent

        user_defined_constituencies: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.user_defined_constituencies, Unset):
            user_defined_constituencies = []
            for user_defined_constituencies_item_data in self.user_defined_constituencies:
                user_defined_constituencies_item = user_defined_constituencies_item_data.to_dict()
                user_defined_constituencies.append(user_defined_constituencies_item)

        student_relation_constituencies: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.student_relation_constituencies, Unset):
            student_relation_constituencies = []
            for student_relation_constituencies_item_data in self.student_relation_constituencies:
                student_relation_constituencies_item = student_relation_constituencies_item_data.to_dict()
                student_relation_constituencies.append(student_relation_constituencies_item)

        user_granted_constitpersonalinfo_edit = self.user_granted_constitpersonalinfo_edit

        name = self.name

        fundraising_group_constituency_text = self.fundraising_group_constituency_text

        social_media_accounts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.social_media_accounts, Unset):
            social_media_accounts = []
            for social_media_accounts_item_data in self.social_media_accounts:
                social_media_accounts_item = social_media_accounts_item_data.to_dict()
                social_media_accounts.append(social_media_accounts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if constituent_profile is not UNSET:
            field_dict["constituent_profile"] = constituent_profile
        if organization is not UNSET:
            field_dict["organization"] = organization
        if address is not UNSET:
            field_dict["address"] = address
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if phone_type is not UNSET:
            field_dict["phone_type"] = phone_type
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if do_not_mail is not UNSET:
            field_dict["do_not_mail"] = do_not_mail
        if do_not_email is not UNSET:
            field_dict["do_not_email"] = do_not_email
        if do_not_phone is not UNSET:
            field_dict["do_not_phone"] = do_not_phone
        if web_address is not UNSET:
            field_dict["web_address"] = web_address
        if related_constituent is not UNSET:
            field_dict["related_constituent"] = related_constituent
        if related_constituent_id is not UNSET:
            field_dict["related_constituent_id"] = related_constituent_id
        if plannedgiverconstituencytext is not UNSET:
            field_dict["plannedgiverconstituencytext"] = plannedgiverconstituencytext
        if bank_constituency_text is not UNSET:
            field_dict["bank_constituency_text"] = bank_constituency_text
        if recognition_constituency_text is not UNSET:
            field_dict["recognition_constituency_text"] = recognition_constituency_text
        if student_enrollment_id is not UNSET:
            field_dict["student_enrollment_id"] = student_enrollment_id
        if student_constituency_text is not UNSET:
            field_dict["student_constituency_text"] = student_constituency_text
        if member_constituency_text is not UNSET:
            field_dict["member_constituency_text"] = member_constituency_text
        if advocate_constituency_text is not UNSET:
            field_dict["advocate_constituency_text"] = advocate_constituency_text
        if board_member_constituency_text is not UNSET:
            field_dict["board_member_constituency_text"] = board_member_constituency_text
        if relation_constituency_text is not UNSET:
            field_dict["relation_constituency_text"] = relation_constituency_text
        if staff_constituency_text is not UNSET:
            field_dict["staff_constituency_text"] = staff_constituency_text
        if donor_constituency_text is not UNSET:
            field_dict["donor_constituency_text"] = donor_constituency_text
        if fundraiser_constituency_text is not UNSET:
            field_dict["fundraiser_constituency_text"] = fundraiser_constituency_text
        if prospect_constituency_text is not UNSET:
            field_dict["prospect_constituency_text"] = prospect_constituency_text
        if volunteer_constituency_text is not UNSET:
            field_dict["volunteer_constituency_text"] = volunteer_constituency_text
        if patron_constituency_text is not UNSET:
            field_dict["patron_constituency_text"] = patron_constituency_text
        if community_member_constituency_text is not UNSET:
            field_dict["community_member_constituency_text"] = community_member_constituency_text
        if user_defined_constituency_text is not UNSET:
            field_dict["user_defined_constituency_text"] = user_defined_constituency_text
        if alumnus_status_text is not UNSET:
            field_dict["alumnus_status_text"] = alumnus_status_text
        if alumnus_enrollment_id is not UNSET:
            field_dict["alumnus_enrollment_id"] = alumnus_enrollment_id
        if alumnus_constituency_text is not UNSET:
            field_dict["alumnus_constituency_text"] = alumnus_constituency_text
        if registrant_status_text is not UNSET:
            field_dict["registrant_status_text"] = registrant_status_text
        if vendor_status_text is not UNSET:
            field_dict["vendor_status_text"] = vendor_status_text
        if inactive is not UNSET:
            field_dict["inactive"] = inactive
        if deceaseddate is not UNSET:
            field_dict["deceaseddate"] = deceaseddate
        if picture is not UNSET:
            field_dict["picture"] = picture
        if primary_education_id is not UNSET:
            field_dict["primary_education_id"] = primary_education_id
        if primary_education is not UNSET:
            field_dict["primary_education"] = primary_education
        if primary_business_id is not UNSET:
            field_dict["primary_business_id"] = primary_business_id
        if primary_business is not UNSET:
            field_dict["primary_business"] = primary_business
        if lookup_id is not UNSET:
            field_dict["lookup_id"] = lookup_id
        if wealthpoint_update_pending is not UNSET:
            field_dict["wealthpoint_update_pending"] = wealthpoint_update_pending
        if education_attribute_defined is not UNSET:
            field_dict["education_attribute_defined"] = education_attribute_defined
        if matchfinder_constituency_text is not UNSET:
            field_dict["matchfinder_constituency_text"] = matchfinder_constituency_text
        if matchfinder_online_record_id is not UNSET:
            field_dict["matchfinder_online_record_id"] = matchfinder_online_record_id
        if solicit_code_count is not UNSET:
            field_dict["solicit_code_count"] = solicit_code_count
        if household_id is not UNSET:
            field_dict["household_id"] = household_id
        if household_text is not UNSET:
            field_dict["household_text"] = household_text
        if group is not UNSET:
            field_dict["group"] = group
        if group_type is not UNSET:
            field_dict["group_type"] = group_type
        if group_member_count is not UNSET:
            field_dict["group_member_count"] = group_member_count
        if household is not UNSET:
            field_dict["household"] = household
        if gives_anonymously is not UNSET:
            field_dict["gives_anonymously"] = gives_anonymously
        if spouse_deceased is not UNSET:
            field_dict["spouse_deceased"] = spouse_deceased
        if dissolved is not UNSET:
            field_dict["dissolved"] = dissolved
        if declarations_on_file is not UNSET:
            field_dict["declarations_on_file"] = declarations_on_file
        if committee_constituency_text is not UNSET:
            field_dict["committee_constituency_text"] = committee_constituency_text
        if committee_member is not UNSET:
            field_dict["committee_member"] = committee_member
        if grantor_constituency_text is not UNSET:
            field_dict["grantor_constituency_text"] = grantor_constituency_text
        if sponsor_constituency_text is not UNSET:
            field_dict["sponsor_constituency_text"] = sponsor_constituency_text
        if nfg_constituency_text is not UNSET:
            field_dict["nfg_constituency_text"] = nfg_constituency_text
        if constituent_inactivity_reason is not UNSET:
            field_dict["constituent_inactivity_reason"] = constituent_inactivity_reason
        if committee_member_constituency_text is not UNSET:
            field_dict["committee_member_constituency_text"] = committee_member_constituency_text
        if faculty_constituency_text is not UNSET:
            field_dict["faculty_constituency_text"] = faculty_constituency_text
        if deceased is not UNSET:
            field_dict["deceased"] = deceased
        if current_enrollment_id is not UNSET:
            field_dict["current_enrollment_id"] = current_enrollment_id
        if current_school is not UNSET:
            field_dict["current_school"] = current_school
        if current_enrollment_id_2 is not UNSET:
            field_dict["current_enrollment_id_2"] = current_enrollment_id_2
        if current_school_2 is not UNSET:
            field_dict["current_school_2"] = current_school_2
        if current_enrollment_id_3 is not UNSET:
            field_dict["current_enrollment_id_3"] = current_enrollment_id_3
        if current_school_3 is not UNSET:
            field_dict["current_school_3"] = current_school_3
        if loyal_donor_constituency_text is not UNSET:
            field_dict["loyal_donor_constituency_text"] = loyal_donor_constituency_text
        if major_donor_constituency_text is not UNSET:
            field_dict["major_donor_constituency_text"] = major_donor_constituency_text
        if student_relation_constituency_text is not UNSET:
            field_dict["student_relation_constituency_text"] = student_relation_constituency_text
        if phone_is_confidential is not UNSET:
            field_dict["phone_is_confidential"] = phone_is_confidential
        if address_is_confidential is not UNSET:
            field_dict["address_is_confidential"] = address_is_confidential
        if constituencies_display_order is not UNSET:
            field_dict["constituencies_display_order"] = constituencies_display_order
        if sponsor_type_code is not UNSET:
            field_dict["sponsor_type_code"] = sponsor_type_code
        if lifecycle_stage is not UNSET:
            field_dict["lifecycle_stage"] = lifecycle_stage
        if lifecycle_stage_as_of is not UNSET:
            field_dict["lifecycle_stage_as_of"] = lifecycle_stage_as_of
        if planned_giver_stage is not UNSET:
            field_dict["planned_giver_stage"] = planned_giver_stage
        if planned_giver_stage_as_of is not UNSET:
            field_dict["planned_giver_stage_as_of"] = planned_giver_stage_as_of
        if donor_state_code is not UNSET:
            field_dict["donor_state_code"] = donor_state_code
        if donor_state is not UNSET:
            field_dict["donor_state"] = donor_state
        if last_revenue_date is not UNSET:
            field_dict["last_revenue_date"] = last_revenue_date
        if address_id is not UNSET:
            field_dict["address_id"] = address_id
        if phone_number_id is not UNSET:
            field_dict["phone_number_id"] = phone_number_id
        if email_address_id is not UNSET:
            field_dict["email_address_id"] = email_address_id
        if top_parent_id is not UNSET:
            field_dict["top_parent_id"] = top_parent_id
        if top_parent is not UNSET:
            field_dict["top_parent"] = top_parent
        if user_defined_constituencies is not UNSET:
            field_dict["user_defined_constituencies"] = user_defined_constituencies
        if student_relation_constituencies is not UNSET:
            field_dict["student_relation_constituencies"] = student_relation_constituencies
        if user_granted_constitpersonalinfo_edit is not UNSET:
            field_dict["user_granted_constitpersonalinfo_edit"] = user_granted_constitpersonalinfo_edit
        if name is not UNSET:
            field_dict["name"] = name
        if fundraising_group_constituency_text is not UNSET:
            field_dict["fundraising_group_constituency_text"] = fundraising_group_constituency_text
        if social_media_accounts is not UNSET:
            field_dict["social_media_accounts"] = social_media_accounts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_constituencies_display_order import ConstituentConstituenciesDisplayOrder
        from ..models.constituent_social_media_accounts import ConstituentSocialMediaAccounts
        from ..models.constituent_student_relation_constituencies import (
            ConstituentStudentRelationConstituencies,
        )
        from ..models.constituent_user_defined_constituencies import ConstituentUserDefinedConstituencies
        from ..models.fuzzy_date import FuzzyDate

        d = src_dict.copy()
        constituent_profile = d.pop("constituent_profile", UNSET)

        organization = d.pop("organization", UNSET)

        address = d.pop("address", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        phone_type = d.pop("phone_type", UNSET)

        email_address = d.pop("email_address", UNSET)

        do_not_mail = d.pop("do_not_mail", UNSET)

        do_not_email = d.pop("do_not_email", UNSET)

        do_not_phone = d.pop("do_not_phone", UNSET)

        web_address = d.pop("web_address", UNSET)

        related_constituent = d.pop("related_constituent", UNSET)

        related_constituent_id = d.pop("related_constituent_id", UNSET)

        plannedgiverconstituencytext = d.pop("plannedgiverconstituencytext", UNSET)

        bank_constituency_text = d.pop("bank_constituency_text", UNSET)

        recognition_constituency_text = d.pop("recognition_constituency_text", UNSET)

        student_enrollment_id = d.pop("student_enrollment_id", UNSET)

        student_constituency_text = d.pop("student_constituency_text", UNSET)

        member_constituency_text = d.pop("member_constituency_text", UNSET)

        advocate_constituency_text = d.pop("advocate_constituency_text", UNSET)

        board_member_constituency_text = d.pop("board_member_constituency_text", UNSET)

        relation_constituency_text = d.pop("relation_constituency_text", UNSET)

        staff_constituency_text = d.pop("staff_constituency_text", UNSET)

        donor_constituency_text = d.pop("donor_constituency_text", UNSET)

        fundraiser_constituency_text = d.pop("fundraiser_constituency_text", UNSET)

        prospect_constituency_text = d.pop("prospect_constituency_text", UNSET)

        volunteer_constituency_text = d.pop("volunteer_constituency_text", UNSET)

        patron_constituency_text = d.pop("patron_constituency_text", UNSET)

        community_member_constituency_text = d.pop("community_member_constituency_text", UNSET)

        user_defined_constituency_text = d.pop("user_defined_constituency_text", UNSET)

        alumnus_status_text = d.pop("alumnus_status_text", UNSET)

        alumnus_enrollment_id = d.pop("alumnus_enrollment_id", UNSET)

        alumnus_constituency_text = d.pop("alumnus_constituency_text", UNSET)

        registrant_status_text = d.pop("registrant_status_text", UNSET)

        vendor_status_text = d.pop("vendor_status_text", UNSET)

        inactive = d.pop("inactive", UNSET)

        _deceaseddate = d.pop("deceaseddate", UNSET)
        deceaseddate: Union[Unset, FuzzyDate]
        if isinstance(_deceaseddate, Unset):
            deceaseddate = UNSET
        else:
            deceaseddate = FuzzyDate.from_dict(_deceaseddate)

        picture = d.pop("picture", UNSET)

        primary_education_id = d.pop("primary_education_id", UNSET)

        primary_education = d.pop("primary_education", UNSET)

        primary_business_id = d.pop("primary_business_id", UNSET)

        primary_business = d.pop("primary_business", UNSET)

        lookup_id = d.pop("lookup_id", UNSET)

        wealthpoint_update_pending = d.pop("wealthpoint_update_pending", UNSET)

        education_attribute_defined = d.pop("education_attribute_defined", UNSET)

        matchfinder_constituency_text = d.pop("matchfinder_constituency_text", UNSET)

        matchfinder_online_record_id = d.pop("matchfinder_online_record_id", UNSET)

        solicit_code_count = d.pop("solicit_code_count", UNSET)

        household_id = d.pop("household_id", UNSET)

        household_text = d.pop("household_text", UNSET)

        group = d.pop("group", UNSET)

        group_type = d.pop("group_type", UNSET)

        group_member_count = d.pop("group_member_count", UNSET)

        household = d.pop("household", UNSET)

        gives_anonymously = d.pop("gives_anonymously", UNSET)

        spouse_deceased = d.pop("spouse_deceased", UNSET)

        dissolved = d.pop("dissolved", UNSET)

        declarations_on_file = d.pop("declarations_on_file", UNSET)

        committee_constituency_text = d.pop("committee_constituency_text", UNSET)

        committee_member = d.pop("committee_member", UNSET)

        grantor_constituency_text = d.pop("grantor_constituency_text", UNSET)

        sponsor_constituency_text = d.pop("sponsor_constituency_text", UNSET)

        nfg_constituency_text = d.pop("nfg_constituency_text", UNSET)

        constituent_inactivity_reason = d.pop("constituent_inactivity_reason", UNSET)

        committee_member_constituency_text = d.pop("committee_member_constituency_text", UNSET)

        faculty_constituency_text = d.pop("faculty_constituency_text", UNSET)

        deceased = d.pop("deceased", UNSET)

        current_enrollment_id = d.pop("current_enrollment_id", UNSET)

        current_school = d.pop("current_school", UNSET)

        current_enrollment_id_2 = d.pop("current_enrollment_id_2", UNSET)

        current_school_2 = d.pop("current_school_2", UNSET)

        current_enrollment_id_3 = d.pop("current_enrollment_id_3", UNSET)

        current_school_3 = d.pop("current_school_3", UNSET)

        loyal_donor_constituency_text = d.pop("loyal_donor_constituency_text", UNSET)

        major_donor_constituency_text = d.pop("major_donor_constituency_text", UNSET)

        student_relation_constituency_text = d.pop("student_relation_constituency_text", UNSET)

        phone_is_confidential = d.pop("phone_is_confidential", UNSET)

        address_is_confidential = d.pop("address_is_confidential", UNSET)

        constituencies_display_order = []
        _constituencies_display_order = d.pop("constituencies_display_order", UNSET)
        for constituencies_display_order_item_data in _constituencies_display_order or []:
            constituencies_display_order_item = ConstituentConstituenciesDisplayOrder.from_dict(
                constituencies_display_order_item_data
            )

            constituencies_display_order.append(constituencies_display_order_item)

        sponsor_type_code = d.pop("sponsor_type_code", UNSET)

        lifecycle_stage = d.pop("lifecycle_stage", UNSET)

        _lifecycle_stage_as_of = d.pop("lifecycle_stage_as_of", UNSET)
        lifecycle_stage_as_of: Union[Unset, datetime.datetime]
        if isinstance(_lifecycle_stage_as_of, Unset):
            lifecycle_stage_as_of = UNSET
        else:
            lifecycle_stage_as_of = isoparse(_lifecycle_stage_as_of)

        planned_giver_stage = d.pop("planned_giver_stage", UNSET)

        _planned_giver_stage_as_of = d.pop("planned_giver_stage_as_of", UNSET)
        planned_giver_stage_as_of: Union[Unset, datetime.datetime]
        if isinstance(_planned_giver_stage_as_of, Unset):
            planned_giver_stage_as_of = UNSET
        else:
            planned_giver_stage_as_of = isoparse(_planned_giver_stage_as_of)

        donor_state_code = d.pop("donor_state_code", UNSET)

        donor_state = d.pop("donor_state", UNSET)

        _last_revenue_date = d.pop("last_revenue_date", UNSET)
        last_revenue_date: Union[Unset, datetime.datetime]
        if isinstance(_last_revenue_date, Unset):
            last_revenue_date = UNSET
        else:
            last_revenue_date = isoparse(_last_revenue_date)

        address_id = d.pop("address_id", UNSET)

        phone_number_id = d.pop("phone_number_id", UNSET)

        email_address_id = d.pop("email_address_id", UNSET)

        top_parent_id = d.pop("top_parent_id", UNSET)

        top_parent = d.pop("top_parent", UNSET)

        user_defined_constituencies = []
        _user_defined_constituencies = d.pop("user_defined_constituencies", UNSET)
        for user_defined_constituencies_item_data in _user_defined_constituencies or []:
            user_defined_constituencies_item = ConstituentUserDefinedConstituencies.from_dict(
                user_defined_constituencies_item_data
            )

            user_defined_constituencies.append(user_defined_constituencies_item)

        student_relation_constituencies = []
        _student_relation_constituencies = d.pop("student_relation_constituencies", UNSET)
        for student_relation_constituencies_item_data in _student_relation_constituencies or []:
            student_relation_constituencies_item = ConstituentStudentRelationConstituencies.from_dict(
                student_relation_constituencies_item_data
            )

            student_relation_constituencies.append(student_relation_constituencies_item)

        user_granted_constitpersonalinfo_edit = d.pop("user_granted_constitpersonalinfo_edit", UNSET)

        name = d.pop("name", UNSET)

        fundraising_group_constituency_text = d.pop("fundraising_group_constituency_text", UNSET)

        social_media_accounts = []
        _social_media_accounts = d.pop("social_media_accounts", UNSET)
        for social_media_accounts_item_data in _social_media_accounts or []:
            social_media_accounts_item = ConstituentSocialMediaAccounts.from_dict(social_media_accounts_item_data)

            social_media_accounts.append(social_media_accounts_item)

        constituent_summary_profile_view = cls(
            constituent_profile=constituent_profile,
            organization=organization,
            address=address,
            phone_number=phone_number,
            phone_type=phone_type,
            email_address=email_address,
            do_not_mail=do_not_mail,
            do_not_email=do_not_email,
            do_not_phone=do_not_phone,
            web_address=web_address,
            related_constituent=related_constituent,
            related_constituent_id=related_constituent_id,
            plannedgiverconstituencytext=plannedgiverconstituencytext,
            bank_constituency_text=bank_constituency_text,
            recognition_constituency_text=recognition_constituency_text,
            student_enrollment_id=student_enrollment_id,
            student_constituency_text=student_constituency_text,
            member_constituency_text=member_constituency_text,
            advocate_constituency_text=advocate_constituency_text,
            board_member_constituency_text=board_member_constituency_text,
            relation_constituency_text=relation_constituency_text,
            staff_constituency_text=staff_constituency_text,
            donor_constituency_text=donor_constituency_text,
            fundraiser_constituency_text=fundraiser_constituency_text,
            prospect_constituency_text=prospect_constituency_text,
            volunteer_constituency_text=volunteer_constituency_text,
            patron_constituency_text=patron_constituency_text,
            community_member_constituency_text=community_member_constituency_text,
            user_defined_constituency_text=user_defined_constituency_text,
            alumnus_status_text=alumnus_status_text,
            alumnus_enrollment_id=alumnus_enrollment_id,
            alumnus_constituency_text=alumnus_constituency_text,
            registrant_status_text=registrant_status_text,
            vendor_status_text=vendor_status_text,
            inactive=inactive,
            deceaseddate=deceaseddate,
            picture=picture,
            primary_education_id=primary_education_id,
            primary_education=primary_education,
            primary_business_id=primary_business_id,
            primary_business=primary_business,
            lookup_id=lookup_id,
            wealthpoint_update_pending=wealthpoint_update_pending,
            education_attribute_defined=education_attribute_defined,
            matchfinder_constituency_text=matchfinder_constituency_text,
            matchfinder_online_record_id=matchfinder_online_record_id,
            solicit_code_count=solicit_code_count,
            household_id=household_id,
            household_text=household_text,
            group=group,
            group_type=group_type,
            group_member_count=group_member_count,
            household=household,
            gives_anonymously=gives_anonymously,
            spouse_deceased=spouse_deceased,
            dissolved=dissolved,
            declarations_on_file=declarations_on_file,
            committee_constituency_text=committee_constituency_text,
            committee_member=committee_member,
            grantor_constituency_text=grantor_constituency_text,
            sponsor_constituency_text=sponsor_constituency_text,
            nfg_constituency_text=nfg_constituency_text,
            constituent_inactivity_reason=constituent_inactivity_reason,
            committee_member_constituency_text=committee_member_constituency_text,
            faculty_constituency_text=faculty_constituency_text,
            deceased=deceased,
            current_enrollment_id=current_enrollment_id,
            current_school=current_school,
            current_enrollment_id_2=current_enrollment_id_2,
            current_school_2=current_school_2,
            current_enrollment_id_3=current_enrollment_id_3,
            current_school_3=current_school_3,
            loyal_donor_constituency_text=loyal_donor_constituency_text,
            major_donor_constituency_text=major_donor_constituency_text,
            student_relation_constituency_text=student_relation_constituency_text,
            phone_is_confidential=phone_is_confidential,
            address_is_confidential=address_is_confidential,
            constituencies_display_order=constituencies_display_order,
            sponsor_type_code=sponsor_type_code,
            lifecycle_stage=lifecycle_stage,
            lifecycle_stage_as_of=lifecycle_stage_as_of,
            planned_giver_stage=planned_giver_stage,
            planned_giver_stage_as_of=planned_giver_stage_as_of,
            donor_state_code=donor_state_code,
            donor_state=donor_state,
            last_revenue_date=last_revenue_date,
            address_id=address_id,
            phone_number_id=phone_number_id,
            email_address_id=email_address_id,
            top_parent_id=top_parent_id,
            top_parent=top_parent,
            user_defined_constituencies=user_defined_constituencies,
            student_relation_constituencies=student_relation_constituencies,
            user_granted_constitpersonalinfo_edit=user_granted_constitpersonalinfo_edit,
            name=name,
            fundraising_group_constituency_text=fundraising_group_constituency_text,
            social_media_accounts=social_media_accounts,
        )

        return constituent_summary_profile_view
